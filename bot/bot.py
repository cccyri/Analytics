import telebot
from telebot import types
from Config import token
import DataBase


bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    DataBase.create_user(message.from_user.username)
    bot.send_message(message.chat.id, "Добро пожаловать! Выберите то, кем вы являетесь", reply_markup=choose_role())


@bot.message_handler(content_types=["text"])
def send_text(message):

    if message.text == 'Представитель IT сферы':
        text = 'Выберите какие категории вам интересны:'
        bot.send_message(message.chat.id, text, reply_markup=choose_category())
    elif message.text == 'Программирование':
        text = 'Выберите категорию:'
        bot.send_message(message.chat.id, text, reply_markup=choose_category1())
    elif message.text == 'Дизайн/Арт':
        text = 'Выберите категорию:'
        bot.send_message(message.chat.id, text, reply_markup=choose_category2())
    elif message.text == 'Аудио/Видео':
        text = 'Выберите категорию:'
        bot.send_message(message.chat.id, text, reply_markup=choose_category3())
    elif message.text == 'Продвижение':
        text = 'Выберите категорию:'
        bot.send_message(message.chat.id, text, reply_markup=choose_category4())
    elif message.text == 'Работа с текстами':
        text = 'Выберите категорию:'
        bot.send_message(message.chat.id, text, reply_markup=choose_category5())
    elif message.text == 'Назад':
        text = 'Выберите категорию:'
        bot.send_message(message.chat.id, text, reply_markup=choose_role())
    elif message.text == 'Верстка сайтов, лендингов' or message.text == 'Разработка лендингов' or message.text == 'Разработка мобильных приложений' or message.text == 'Разработка парсеров, парсинг' \
        or message.text == 'Разработка сайтов' or message.text == 'Разработка чат-ботов' or message.text == '3D моделирование' or message.text == 'Дизайн визиток, баннеров, фирм. стиль' or message.text == 'Дизайн логотипов' \
        or message.text == 'Дизайн мобильных приложений' or message.text == 'Дизайн сайтов, лендингов' or message.text == 'Оформление соц.сетей' or message.text == 'Озвучка' or message.text == 'Создание видео, видео-монтаж' \
        or message.text == 'SEO-специалист' or message.text == 'Контекстная реклама' or message.text == 'Таргетированная реклама' or message.text == 'Копирайтинг' or message.text == 'Рерайтинг' or message.text == 'Транскрибация':
        text = f'Вам будут показываться задания по тематике {message.text}'
        DataBase.add_category(message.from_user.username, message.text)
        bot.send_message(message.chat.id, text, reply_markup=after_category())
    elif message.text == 'Выбрать другую категорию':
        text = 'Выберите категорию:'
        bot.send_message(message.chat.id, text, reply_markup=choose_category())



@bot.callback_query_handler(func=lambda message: True)
def choose_role():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Представитель IT сферы')
    btn2 = types.KeyboardButton('Представитель НКО')
    markup.add(btn1).add(btn2)
    return markup


def choose_category():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Программирование')
    btn2 = types.KeyboardButton('Дизайн/Арт')
    btn3 = types.KeyboardButton('Аудио/Видео')
    btn4 = types.KeyboardButton('Продвижение')
    btn5 = types.KeyboardButton('Работа с текстами')
    btn6 = types.KeyboardButton('Назад')
    markup.add(btn1).add(btn2).add(btn3).add(btn4).add(btn5).add(btn6)
    return markup

def choose_category1():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Верстка сайтов, лендингов')
    btn2 = types.KeyboardButton('Разработка лендингов')
    btn3 = types.KeyboardButton('Разработка мобильных приложений')
    btn4 = types.KeyboardButton('Разработка парсеров, парсинг')
    btn5 = types.KeyboardButton('Разработка сайтов')
    btn6 = types.KeyboardButton('Разработка чат-ботов')
    btn7 = types.KeyboardButton('Назад')
    markup.add(btn1).add(btn2).add(btn3).add(btn4).add(btn5).add(btn6).add(btn7)
    return markup


def choose_category2():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('3D моделирование')
    btn2 = types.KeyboardButton('Дизайн визиток, баннеров, фирм. стиль')
    btn3 = types.KeyboardButton('Дизайн логотипов')
    btn4 = types.KeyboardButton('Дизайн мобильных приложений')
    btn5 = types.KeyboardButton('Дизайн сайтов, лендингов')
    btn6 = types.KeyboardButton('Оформление соц.сетей')
    btn7 = types.KeyboardButton('Назад')
    markup.add(btn1).add(btn2).add(btn3).add(btn4).add(btn5).add(btn6).add(btn7)
    return markup


def choose_category3():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Озвучка')
    btn2 = types.KeyboardButton('Создание видео, видео-монтаж')
    btn3 = types.KeyboardButton('Назад')
    markup.add(btn1).add(btn2).add(btn3)
    return markup


def choose_category4():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('SEO-специалист')
    btn2 = types.KeyboardButton('Контекстная реклама')
    btn3 = types.KeyboardButton('Таргетированная реклама')
    btn4 = types.KeyboardButton('Назад')
    markup.add(btn1).add(btn2).add(btn3).add(btn4)
    return markup


def choose_category5():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Копирайтинг')
    btn2 = types.KeyboardButton('Рерайтинг')
    btn3 = types.KeyboardButton('Транскрибация')
    btn4 = types.KeyboardButton('Назад')
    markup.add(btn1).add(btn2).add(btn3).add(btn4)
    return markup

def after_category():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Выбрать другую категорию')
    markup.add(btn1)
    return markup



bot.polling(none_stop=True)