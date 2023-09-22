import telebot
import sqlite3
import datetime

# Инициализация бота
bot = telebot.TeleBot('6332254106:AAE8D3drBAJAU1RSYL9i3Dj4d0SalVOwiu4')

# Функция для подключения к базе данных
def connect_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    return conn, cursor

# Создаем таблицу для хранения информации о пользователях
conn, cursor = connect_db()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        chat_id INTEGER,
        user_id TEXT,
        username TEXT,
        full_name TEXT,
        status TEXT,
        going BOOLEAN
    )
''')
conn.commit()
conn.close()


# Определение функций обработчиков команд и сообщений

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user_id = message.chat.username

    markup = telebot.types.ReplyKeyboardRemove(selective=False)
    msg = bot.send_message(chat_id, "Дорогой гость, назовите Ваше имя.", reply_markup=markup)
    bot.register_next_step_handler(msg, lambda message: process_full_name(message, user_id, chat_id))

def process_full_name(message, user_id, chat_id):
    username = message.text

    markup = telebot.types.ReplyKeyboardRemove(selective=False)
    msg = bot.send_message(chat_id, "Назовите Вашу фамилию.", reply_markup=markup)
    if user_id == "manulmauch" or user_id == "osssip" or user_id == "hazzarak":
        bot.register_next_step_handler(msg, lambda message: process_final("Королевский цербер", user_id, chat_id, username, message.text))
    else:
        if user_id == "LelyKalinina":
            bot.register_next_step_handler(msg, lambda message: process_final("Крёстная фея", user_id, chat_id, username, message.text))
        else:
            if user_id == "clip_iv_fox":
                bot.register_next_step_handler(msg, lambda message: process_final("С величайшей гордостью представляю вам владыку ночи и хозяина этого волшебного дворца, Да здравствует король бала", user_id, chat_id, username, message.text))
            else:
                if user_id == "tareny" or user_id == "MrAlexandrov":
                    bot.register_next_step_handler(msg, lambda message: process_final("Глашатай ада", user_id, chat_id, username, message.text))
                else:
                    bot.register_next_step_handler(msg, lambda message: process_status(message, user_id, chat_id, username))

def process_status(message, user_id, chat_id, username):
    full_name = message.text

    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, selective=False)
    markup.add(
        'Герцог',
        "Герцогиня",
        'Маркиз',
        "Маркиза",
        'Граф',
        "Графиня",
        'Барон',
        "Баронесса",
        "Визирь",
        "Визиресса",
        "Лорд",
        "Леди",
        "Князь",
        "Княгиня",
        "Император",
        "Императрица",
        "Патриарх",
        "Матриарх",
        "Владыка",
        "Владычица",
        "Султан",
        "Султанесса",
        "Царь",
        "Царица",
        "Принц",
        "Принцесса",
        "Дон",
        "Донна",
        "Аристократ",
        "Аристократка",
        "Сеньор",
        "Сеньора",
        "Консул",
        "Консулесса",
        "Воевода",
        "Воеводиха",
        "Сенатор",
        "Сенаторша"
    )
    # Send the message with the keyboard
    msg = bot.send_message(chat_id, "Какой у Вас Статус?", reply_markup=markup)
    # Register the next step handler
    bot.register_next_step_handler(msg, lambda message: process_final(message.text, user_id, chat_id, username, full_name))

def insert_user(chat_id, user_id, username, full_name, status):
    king_id = get_heraldus_id("clip_iv_fox")
    message_to_send = f" Статус: {status}\nИмя: {username}\nФамилия: {full_name}\n"
    if king_id is not None: bot.send_message(king_id, message_to_send)

    conn, cursor = connect_db()
    cursor.execute('''INSERT INTO users (chat_id, user_id, username, full_name, status, going)
                VALUES (?, ?, ?, ?, ?, ?)''', (chat_id, user_id, username, full_name, status, False))
    conn.commit()
    conn.close()

# В функции process_final
def process_final(status, user_id, chat_id, username, full_name):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, selective=False)
    markup.add('Я захожу')
    insert_user(chat_id, user_id, username, full_name, status)
    bot.send_message(chat_id, f"Спасибо, в период с 6 до 8 вечера 7 октября нажмите кнопку \"Я захожу\", чтобы глашатай вас представил, учитывая информацию о вас:\n\n"
                                f"{status} {username} {full_name}", reply_markup=markup)

def get_user_info(user_id):
    conn, cursor = connect_db()
    cursor.execute('SELECT username, full_name, status FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0], result[1], result[2]
    else:
        return None, None, None

def get_heraldus_id(user_id):
    conn, cursor = connect_db()
    cursor.execute('SELECT chat_id FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0]
    else:
        return None

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    chat_id = message.chat.id
    user_id = message.chat.username
    text = message.text

    current_time = datetime.datetime.now().time()
    current_date = datetime.datetime.now().date()

    if text == 'Я захожу':
        if current_date == datetime.date(2023, 10, 7) and current_time >= datetime.time(18, 0) and current_time < datetime.time(20, 0):
            name, full_name, status = get_user_info(user_id)
            king_id = get_heraldus_id("clip_iv_fox")
            heraldus_id_1 = get_heraldus_id("tareny")
            heraldus_id_2 = get_heraldus_id("MrAlexandrov")
            markup = telebot.types.ReplyKeyboardRemove(selective=False)

            if full_name is not None and status is not None and status is not None:
                message_to_send = f" Статус: {status}\nИмя: {name}\nФамилия: {full_name}\n"
                bot.send_message(chat_id, "Глашатай Вас объявляет, заходите!", reply_markup=markup)
                if king_id is not None: bot.send_message(king_id, message_to_send)
                if heraldus_id_1 is not None: bot.send_message(heraldus_id_1, message_to_send)
                if heraldus_id_2 is not None: bot.send_message(heraldus_id_2, message_to_send)
            else:
                bot.send_message(chat_id, "К сожалению, не удалось найти Вашу информацию.")
        else:
            markup = telebot.types.ReplyKeyboardRemove(selective=False)
            bot.send_message(chat_id, "К сожалению, сейчас не время прибытия.")
    else:
        bot.send_message(chat_id, "Вы отправили неверное сообщение, повторите.")


# Запускаем бота
bot.polling(none_stop=True, timeout=0)