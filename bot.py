import telebot
import calendar
import time
import emoji
import requests

from telebot import types
from datetime import datetime, timezone
from dateutil.parser import parse
from requests.adapters import HTTPAdapter

bot = telebot.TeleBot('5966874038:AAEafXea9Sj4v0hBU8Fjd0joqhctG2loW5Y')

timestamp = calendar.timegm(time.gmtime())
photo_url = f"http://oblenergo.cv.ua/shutdowns/GPV.png?ver={timestamp}"

markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
site = types.KeyboardButton('Сайт Обленерго 💻')
schedule = types.KeyboardButton('Актуальний Графік 📊')
notif = types.KeyboardButton('Сповіщення 🔔')
help = types.KeyboardButton('Тех. Підтримка 🔧')
markup.add(site, schedule, notif, help)

@bot.message_handler(commands=['start'])
def start(message):
    text = f'Привіт, <b>{message.from_user.first_name}</b> 👋 Чим можу бути корисним?'
    bot.send_message(message.chat.id, text, parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def send_info(message):
    if message.text=='Сайт Обленерго 💻':
        bot.send_message(message.chat.id, 'http://oblenergo.cv.ua/', parse_mode='html')
    elif message.text=='Актуальний Графік 📊':
        bot.send_photo(message.chat.id, photo=photo_url)

    markup_answer = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    yes = types.KeyboardButton('Так ✅')
    no = types.KeyboardButton('Ні ❌')
    markup_answer.add(yes, no)

    if message.text=='Сповіщення 🔔':
        bot.send_message(message.chat.id, 'Чи бажаєте отримувати сповіщення щоразу коли графік оновлюватиметься?', parse_mode='html', reply_markup=markup_answer)

    if message.text=='Так ✅':
        bot.send_message(message.chat.id, 'Тепер ви будете отримувати сповіщення щоразу коли графік оновлюватиметься 😉', parse_mode='html', reply_markup=markup)
        last_photo_date = datetime.now(timezone.utc)
        print('start checking for new image')
        while True:
            try:
                timestamp = calendar.timegm(time.gmtime())
                photo_url1 = f"http://oblenergo.cv.ua/shutdowns/GPV.png?ver={timestamp}"
                print(f'checking {photo_url1}')
                r = requests.get(photo_url1, verify=False, stream=True, timeout=60)
                current_photo_date = parse(r.headers['Last-Modified'])
                print(f'{current_photo_date=}')
                if current_photo_date > last_photo_date:
                    print(f'{last_photo_date=}')
                    # photo changed, so do something like send the new changed photo
                    bot.send_photo(message.chat_id, photo=photo_url1, timeout=60)
                    bot.send_message(message.chat.id, '🔴 Графік Оновився!', parse_mode='html')

                    last_photo_date = current_photo_date # update to last sent photo, so we don't send same photo again.
            except Exception:
                print('while error')
            time.sleep(60) # sleep for 1 minutes then check again
    
    if message.text=='Ні ❌':
        bot.send_message(message.chat.id, 'Гаразд 😕', parse_mode='html', reply_markup=markup)   
   
   
    markup_help = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    issue = types.KeyboardButton('Знайшов/ла помилку 😬')
    suggest = types.KeyboardButton('Знаю як покращити бота 😏')
    nothing = types.KeyboardButton('Нічого, випадково натиснув/ла сюди 😅')
    markup_help.add(issue, suggest, nothing)

    if message.text=='Тех. Підтримка 🔧':
        bot.send_message(message.chat.id, 'Що сталося? 🤔', parse_mode='html', reply_markup=markup_help)

    if message.text==('Знайшов/ла помилку 😬'):
        bot.send_message(message.chat.id, 'Зверніться, будь ласка, до мого творця - @shineqwen.', parse_mode='html', reply_markup=markup)
    if message.text==('Знаю як покращити бота 😏'):
        bot.send_message(message.chat.id, 'Зверніться, будь ласка, до мого творця - @shineqwen.', parse_mode='html', reply_markup=markup)
    if message.text==('Нічого, випадково натиснув/ла сюди 😅'):
        bot.send_message(message.chat.id, 'Гаразд)', parse_mode='html', reply_markup=markup)

bot.polling(non_stop=True)