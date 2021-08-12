import vk
import requests
import csv
import random
import time
from datetime import datetime
import pickle
import json

def strTimeProp(start, end, format, prop):

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))

def randomDate(start, end, prop):
    return strTimeProp(start, end, '%Y/%m/%d', prop)

def dateNow():
    return (str(datetime.now())).split(' ')[0]

def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y/%m/%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    #return abs((d2 - d1).days) # в днях
    return abs((d2.year - d1.year))

def CharDateToIntDate(char_date):
    if char_date == None:
        return None
    else:
        return days_between(char_date, dateNow())



token = 'API token here'
community_id = 'miptfpmi' #the id of the community to be investigated

def get_person_information(id):
    response = requests.get('https://api.vk.com/method/users.get?', params={
        'fields': 'sex',
        'user_id': id,
        'access_token': token,
        'v': 5.103
    })
    return (response.json()['response'])[0]

def scan_community(id): # возвращает список id-шников участников группы
    api = vk.Api(token)
    group = api.get_group(id)
    user_items = [user for user in group.get_members_only_id()]
    return user_items

def get_person_friends(id): # возвращает список id-шников друзей у данного человека
    friends = requests.get('https://api.vk.com/method/friends.get?', params={
        #'fields': 'sex',
        'user_id': id,
        'access_token': token,
        'v': '5.130'
    })
    if list(friends.json().keys())[0] == 'error':
        return 'This account is private'
    return (friends.json()['response'])['items']

def create_UsersIdTxt(list): # заполняет файл id-шниками участников группы (принимает на вход список id участников)
    f = open('users_id.txt', 'w')
    for i in range(len(list)):
        f.write(str(list[i]) + '\n')
    f.close()

def create_FriensIdTxt(list): # заполняет файл по типу участник и его друзья в одной строке
    # (принимает на вход список id участников и размер (сколько участников считать))
    f = open('friends_id.txt', 'w')
    for i in range(len(list)):
        friends = get_person_friends(list[i])
        print(str(list[i]) + ':' + str(friends))
        if friends != 'This account is private':
            f.write(str(list[i]) + ' ')
            for j in range(len(friends)):
                f.write(str(friends[j]) + ' ')
            f.write('\n')
    f.close()

def create_UsersSexTxt(list):
    f = open('users_sex.txt', 'w')
    for i in range(10):
        pers_sex = (get_person_information(str(list[i])))['sex']
        f.write(str(list[i]) + ' ' + str(pers_sex) + '\n')
        print(str((get_person_information(str(list[i])))['first_name']) + ' '
              + str((get_person_information(str(list[i])))['last_name']) + ' '
              + str((get_person_information(str(list[i])))['sex']))
    f.close()


def DictId(): # функция записывает в файл dict_id.json словарь, состоящий из уникальных значений id
    data = []
    with open("friends_id.txt") as f:
        for line in f:
            data.append([x for x in line.split()])
    f.close()

    pers_list = list()
    for i in range(len(data)):
        pers_list = pers_list + data[i]
    unique_pers_list = list(set(pers_list))

    pers_dict = {unique_pers_list[i]: i for i in range(len(unique_pers_list))}
    j = json.dumps(pers_dict)
    with open('dict_id.json', 'w') as f:
        f.write(j)
    f.close()

def create_FriendsAgeCsv():
    with open('dict_id.json', 'r') as f1:
        d_id = json.loads(f1.read())
    f1.close()
    dict_keys = list(d_id.keys()) # все уникальные id-шники

    data = []
    with open("friends_id.txt") as f2:
        for line in f2:
            data.append([x for x in line.split()])
    f2.close()

    users_id = [x[0] for x in data] # пользователи сообщества
    mat = [line[1:] for line in data[:]] # матрица друзей (data без первого столбца)
    fr = list()
    for i in range(len(mat)):
        fr = fr + mat[i]
    friends = list(set(fr)) # список друзей
    mat.clear()
    fr.clear()
    data.clear()

    f3 = open('_friends_age.csv', mode="w", encoding='utf-8')
    file_writer = csv.writer(f3, delimiter=",", lineterminator="\r")
    file_writer.writerow(['Id', 'Age'])
    for i in range(len(d_id)):
        age = CharDateToIntDate(randomDate("1988/01/01", "2007/01/01", random.random()))
        file_writer.writerow([str(d_id[dict_keys[i]]), age])

def create_ParticularsCsv(): # создает файл с информацией о вершинах
    with open('dict_id.json', 'r') as f1:
        d_id = json.loads(f1.read())
    f1.close()
    dict_keys = list(d_id.keys()) # все уникальные id-шники

    data = []
    with open("friends_id.txt") as f2:
        for line in f2:
            data.append([x for x in line.split()])
    f2.close()

    users_id = [x[0] for x in data] # пользователи сообщества
    mat = [line[1:] for line in data[:]] # матрица друзей (data без первого столбца)
    fr = list()
    for i in range(len(mat)):
        fr = fr + mat[i]
    friends = list(set(fr)) # список друзей
    mat.clear()
    fr.clear()
    data.clear()

    f3 = open('particulars.csv', mode="w", encoding='utf-8')
    file_writer = csv.writer(f3, delimiter=",", lineterminator="\r")
    file_writer.writerow(['Id', 'Age', 'Sex'])
    for i in range(len(dict_keys)):
        if dict_keys[i] in users_id: # является ли id-шник пользователем сообщества
            pers_sex = (get_person_information(str(dict_keys[i])))['sex']
            if dict_keys[i] in friends: # является ли id-шник еще и чьим-то другом
                age = CharDateToIntDate(randomDate("1988/01/01", "2007/01/01", random.random()))
                file_writer.writerow([str(d_id[dict_keys[i]]), age, str(pers_sex)])
                #print(str(d_id[dict_keys[i]]) + ' ' + str(age) + ' ' + str(pers_sex))
            else: # id-шник не является чьи-то другом
                age = CharDateToIntDate(randomDate("1988/01/01", "2007/01/01", random.random()))
                file_writer.writerow([str(d_id[dict_keys[i]]), age, str(pers_sex)])
                #print(str(d_id[dict_keys[i]]) + ' ' + str(age) + ' ' + str(pers_sex))
        else: # id-шник не пользователь сообщества
            age = CharDateToIntDate(randomDate("1988/01/01", "2007/01/01", random.random()))
            file_writer.writerow([str(d_id[dict_keys[i]]), age, -1])
    dict_keys.clear()
    users_id.clear()
    friends.clear()
    f3.close()

def create_AgeVectorCsv():

    pers_age = list() # матрица из возростов людей:(id, age)
    with open('particulars.csv') as File:
        reader = csv.reader(File, delimiter=',', quotechar=',')
        for row in reader:
            content = list(row[i] for i in range(2))
            pers_age.append(content)
    pers_age.pop(0)

    f3 = open('_age_vector.csv', mode="w", encoding='utf-8')
    file_writer = csv.writer(f3, delimiter=",", lineterminator="\r")
    file_writer.writerow(['Id', 'Age[0;15)', 'Age[15;20)', 'Age[20;25)', 'Age[25;30)', 'Age[30;35)', 'Age[35;45)', 'Age[45;inf)'])
    for i in range(len(pers_age)):
        if int(pers_age[i][1]) < 15:
            file_writer.writerow([pers_age[i][0], 1, 0, 0, 0, 0, 0, 0])
        elif int(pers_age[i][1]) < 20:
            file_writer.writerow([pers_age[i][0], 0, 1, 0, 0, 0, 0, 0])
        elif int(pers_age[i][1]) < 25:
            file_writer.writerow([pers_age[i][0], 0, 0, 1, 0, 0, 0, 0])
        elif int(pers_age[i][1]) < 30:
            file_writer.writerow([pers_age[i][0], 0, 0, 0, 1, 0, 0, 0])
        elif int(pers_age[i][1]) < 35:
            file_writer.writerow([pers_age[i][0], 0, 0, 0, 0, 1, 0, 0])
        elif int(pers_age[i][1]) < 45:
            file_writer.writerow([pers_age[i][0], 0, 0, 0, 0, 0, 1, 0])
        elif int(pers_age[i][1]) >= 45:
            file_writer.writerow([pers_age[i][0], 0, 0, 0, 0, 0, 0, 1])

def create_DataCsv(): # создает файл смежности вершин
    with open('dict_id.json', 'r') as f1:
        d_id = json.loads(f1.read())
    f1.close()

    data = []
    with open("friends_id.txt") as f2:
        for line in f2:
            data.append([x for x in line.split()])
    f2.close()

    f3 = open('data.csv', mode="w", encoding='utf-8')
    file_writer = csv.writer(f3, delimiter=",", lineterminator="\r")
    file_writer.writerow(['Src', 'Dst', 'Weight'])
    for i in range(len(data)):
        for j in range(1, len(data[i])):
            file_writer.writerow([d_id[data[i][0]], d_id[data[i][j]], 1])
        for j in range(1, len(data[i])):
            file_writer.writerow([d_id[data[i][j]], d_id[data[i][0]], 1])
    data.clear()
    f3.close()


def DictId_2(): # функция записывает в файл dict_id_2.json словарь, состоящий из уникальных значений id

    f = open('friends_id.txt', 'r')
    lines = f.readlines()
    f_column_number = 0
    pers_list = []
    for x in lines:
        pers_list.append(x.split()[f_column_number])
    f.close()

    pers_dict = {pers_list[i]: i for i in range(len(pers_list))}
    j = json.dumps(pers_dict)
    with open('dict_id_2.json', 'w') as f1:
        f1.write(j)
    f1.close()

def create_FriendlyTiesTxt(): # создает txt файл с информацией о дружественных связях внутри сообщества
    with open('dict_id_2.json', 'r') as f1:
        d_id = json.loads(f1.read())
    f1.close()
    dict_keys = list(d_id.keys()) # все уникальные id-шники

    data = []
    ties = open("friendly_ties.txt", 'w')
    with open("friends_id.txt") as f2:
        for line in f2:
            data.append([x for x in line.split()])
            for i in range(len(data[0])):
                if data[0][i] in dict_keys:
                    ties.write(str(data[0][i]) + ' ')
            ties.write('\n')
            data.clear()
    ties.close()
    f2.close()

def create_DataCsv_2(): # создает файл смежности вершин
    with open('dict_id_2.json', 'r') as f1:
        d_id = json.loads(f1.read())
    f1.close()

    data = []
    with open("friendly_ties.txt") as f2:
        for line in f2:
            data.append([x for x in line.split()])
    f2.close()

    f3 = open('data_2.csv', mode="w", encoding='utf-8')
    file_writer = csv.writer(f3, delimiter=",", lineterminator="\r")
    file_writer.writerow(['Src', 'Dst', 'Weight'])
    for i in range(len(data)):
        for j in range(1, len(data[i])):
            file_writer.writerow([d_id[data[i][0]], d_id[data[i][j]], 1]) # записываем в data2csv айди чела а потом
                                                                          # все j его друзей которые тоже участники группы
                                                                          #  закидываем на каждой итерации кортеж из 1) айди чела 2) айди j-того друга в группе 3) вес ребра 1
        for j in range(1, len(data[i])):
            file_writer.writerow([d_id[data[i][j]], d_id[data[i][0]], 1]) # то же самое для других ребер
    data.clear()
    f3.close()

def create_UsersSexVectorCsv(): # создает файл txt с полом всех участников сообщества

    with open('dict_id_2.json', 'r') as f1:
        d_id = json.loads(f1.read())
    f1.close()
    dict_keys = list(d_id.keys()) # все уникальные id-шники

    f2 = open('_users_sex.csv', mode="w", encoding='utf-8')
    file_writer = csv.writer(f2, delimiter=",", lineterminator="\r")
    file_writer.writerow(['Id', 'Man', 'Woman', 'NoSex'])
    for i in range(len(dict_keys)):
        pers_sex = (get_person_information(str(dict_keys[i])))['sex']
        #print(str(d_id[str(dict_keys[i])]) + ' ' + str(pers_sex))
        if pers_sex == 1:
            file_writer.writerow([str(d_id[str(dict_keys[i])]), '0', '1', '0'])
        elif pers_sex == 2:
            file_writer.writerow([str(d_id[str(dict_keys[i])]), '1', '0', '0'])
        else:
            file_writer.writerow([str(d_id[str(dict_keys[i])]), '0', '0', '1'])
            #print(dict_keys[i])
    f2.close()


fpmi_users_id = scan_community(community_id)
create_FriensIdTxt(fpmi_users_id[:200])
DictId_2()
create_FriendlyTiesTxt()
create_DataCsv_2()
create_UsersSexVectorCsv()


def run():
    fpmi_users_id = scan_community(community_id) # считываю сообщество
    create_FriensIdTxt(fpmi_users_id, 200) # и создаю текстовый файл с информацией о друзьях пользователей
    DictId() # присваиваю каждому id - шнику уникальный номер
    create_DataCsv() # создаю файл список смежности ребер
    create_ParticularsCsv() # создаю файл признаки вершин
    create_AgeVectorCsv() # файл векторов признаков
