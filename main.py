# Version 1.0
import telebot # Библиотека бота telebot.
import random # Используется для отправки рандом фото и сообщений если нету ответа у бота на него.
import os # Для того чтобы читал файл из папок и тд.
import datetime # Показывает время и дату. Это, для того чтобы вести лог работы бота в файлы message.log bot.log
import difflib # Для того чтобы бот быстрее искал ответы на вопросы в файле Answer_database.txt
"""
========================================================================================================================
                          Выводит красивый текст в консоли
========================================================================================================================
"""
# Для оформления красивого запуска в консоли  установка pip install colorama
import colorama
from colorama import Fore, Style

colorama.init()

def print_colored_text(text, color):
    colored_text = f"{color}{text}{Style.RESET_ALL}"
    print(colored_text)


# Выводит 3D текст "M - Tech IHA Bot" оранжевым цветом
print_colored_text("M - Tech IHA Bot", Fore.LIGHTYELLOW_EX + Style.BRIGHT)
print("Version 1.0")
# Токент бота
bot = telebot.TeleBot('ваш токен')

# Директория, где находится файл с базой ответов для бота
answer_file = os.path.join("database", "Answer_database.txt")

"""
========================================================================================================================
                                     Лог бота
========================================================================================================================
"""

# Перезаписывает файл после перезагрузки бота.
def get_messages_count():
    with open("Logs/bot.log", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                return int(line.split(":")[1].replace(" ", ""))
    return 0

# Пишет в лог бота на сколько он ответил сообщений за все время своей работы
def save_log(bot_log_message):
    with open("Logs/bot.log", "w", encoding="utf-8") as f:
        f.write(f"Дата запуска: {datetime.datetime.now()}\nСообщений принято: {bot_log_message}\n")


# Сохраняет последние сообщения которые писали боту и кому он ответил.
def save_message(message):
    now = datetime.datetime.now()
    with open("Logs/message.log", "a", encoding="utf-8") as f:
        f.write(f"{now} {message.from_user.username} {message.text}\n")
        f.write(f"Бот успешно ответил на сообщение пользователя: {message.from_user.username}\n")


messages_count = 0  # Устанавливаем количество сообщений в 0 при каждом запуске
save_log(messages_count)  # Перезаписываем файл с обновленным количеством сообщений
# Выводит сообщение в консоль при запуске
print("Бот успешно запущен. Сообщений принято:", messages_count)


"""
========================================================================================================================
    Написал код который читает базу ответов из файла: Answer_database.txt
    Пример базы: Привет||Привет, я M - Tech IHA Bot.
    Если бот не знает ответ на сообщение то он выбирает любой вопрос или ответ из файла: Answers_database.txt 
    Базу ответов поддерживает только до 10 мб для более корректной работы бота. 
========================================================================================================================
"""

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global messages_count
    messages_count += 1
    save_log(messages_count)
    save_message(message)

    print(f"Пользователь {message.from_user.username} прислал сообщение: {message.text}")  # Выводит в консоли имя пользователя и его сообщение
    print(f"Бот ответил на сообщение пользователя: {message.from_user.username}")  # Выводит в консоли что бот ответил на сообщение пользователя

    question = message.text
    response_options = get_response_options(question)
    if response_options:
        response = random.choice(response_options)
        bot.send_chat_action(message.chat.id, 'typing')  # печатает
        bot.send_message(message.chat.id, response)
    else:
        random_response = get_random_response()
        bot.send_chat_action(message.chat.id, 'typing')  # печатает
        bot.send_message(message.chat.id, random_response)


def get_response_options(question):
    response_options = []
    file_size = os.path.getsize(answer_file)  # Получить размер файла в байтах
    if file_size <= 10 * 1024 * 1024:  # Проверить, не превышает ли размер 10 МБ
        with open(answer_file, "r", encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line:
                    line_question, line_response = line.split("||")
                    similarity = difflib.SequenceMatcher(None, question.lower(), line_question.lower()).ratio()
                    if similarity > 0.8:
                        response_options.append(line_response)
        return response_options
    else:
        print("Файл ответов слишком большой (превышает 10 МБ). Чтение невозможно.")
        return []


def get_random_response():
    file_size = os.path.getsize(answer_file)  # Получить размер файла в байтах
    if file_size <= 10 * 1024 * 1024:  # Проверить, не превышает ли размер 10 МБ
        with open(answer_file, "r", encoding="utf-8") as file:
            lines = file.readlines()
            random_line = random.choice(lines)
            random_response = random_line.split("||")[1].strip()
            return random_response
    else:
        print("Файл ответов слишком большой (превышает 10 МБ). Чтение невозможно.")
        return []


# запуск бота
bot.polling(none_stop=True)
