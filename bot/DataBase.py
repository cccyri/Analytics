import pymysql.cursors
from Config import host, user, password, database
from datetime import datetime, timedelta
connection = pymysql.connect(host=host, user=user, password=password, database=database, cursorclass=pymysql.cursors.DictCursor)

cursor = connection.cursor()


def create_user(username):
    query = f"select * from users where username = '{username}'"
    cursor.execute(query)
    if cursor.rowcount == 0:
        query = f"insert into users values ('{username}', NULL, 0)"
        cursor.execute(query)
        connection.commit()
    else:
        exit()


def add_category(username, role):
    query = f"update users set role = '{role}' where username = '{username}'"
    cursor.execute(query)
    connection.commit()





def get_balance(username):
    query = f"select balance from users where username = '{username}'"
    cursor.execute(query)
    result = cursor.fetchone()['balance']
    return result

def withdraw(username, sum):
    query = f"select wallet from users where username = '{username}'"
    cursor.execute(query)
    wallet = cursor.fetchone()['wallet']
    query = f"insert into withdraw values ('{username}', '{wallet}', {sum})"
    cursor.execute(query)
    query = f"update users set balance = balance - {sum} where username = '{username}'"
    cursor.execute(query)
    print('Success!')
    connection.commit()

def create_deposit(username, level, sum):
    start_data = datetime.now()
    if (level == 1):
        end_data = start_data + timedelta(days=1)
        final_sum = sum*1.012
    elif (level == 2):
        end_data = start_data + timedelta(days=7)
        final_sum = sum * 1.091
    elif (level == 3):
        end_data = start_data + timedelta(days=14)
        final_sum = sum * 1.190
    elif (level == 4):
        end_data = start_data + timedelta(days=28)
        final_sum = sum * 1.418
    query = f"insert into deposit values ('{username}', {sum}, {level}, '{start_data}', '{end_data}', 1, {final_sum})"
    cursor.execute(query)
    print('Success!')
    query = f"update users set balance = balance - {sum} where username = '{username}'"
    cursor.execute(query)
    connection.commit()

def check_deposit(username):
    now = datetime.now()
    query = f"select * from deposit where status = 1 and username = '{username}'"
    cursor.execute(query)
    num = cursor.rowcount
    result = cursor.fetchall()
    for i in range(num):
        if (result[i]['end_data'] <= now):
            sum = result[i]['final_sum']
            query = f"update users set balance = balance + {sum} where username = '{username}'"
            cursor.execute(query)
            query = f"update deposit set status = 2 where username = '{username}' and end_data = '{result[i]['end_data']}'"
            cursor.execute(query)
            connection.commit()


def active_deposit(username):
    text = '🗒 Список активных депозитов: \n \n'
    query = f"select * from deposit where status = 1 and username = '{username}'"
    cursor.execute(query)
    num = cursor.rowcount
    result = cursor.fetchall()
    for i in range(num):
        text = text + f'▫️ Депозит на {result[i]["sum"]} рублей, который заканчивается {result[i]["end_data"]} и вы получите {result[i]["final_sum"]}\n \n'
    return text