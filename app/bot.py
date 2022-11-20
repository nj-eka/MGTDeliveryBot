import os
from datetime import date
import telebot as tb
from telebot import types
import asyncio
import logging

from keyboards import generate_calendar_days, generate_calendar_months, EMTPY_FIELD
from filters import calendar_factory, calendar_zoom, bind_filters

bot = tb.TeleBot("5637186029:AAEUYNg2QFbDNMD67RzgENDiZm-KjzXZ48w", parse_mode=None)
# bot = tb.TeleBot(os.environ.get("TBOT_TOKEN"), parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN

users = {}

#todo: remove to redis
courier_users = {}

new_courier = {
    'ФИО': None,
    'Номер телефона': None,
    'Маршруты': [[[55.702999, 37.530874], [55.751426, 37.618879]], [[55.704907, 37.640378], [55.819721, 37.611704]]]
}

#

# handlers

@bot.message_handler(func=lambda msg: 'start' in msg.text or 'Назад' in msg.text)
def send_welcome(message):
    if message.from_user.id not in users:
        users[message.from_user.id] = {}
        if 'username' in users[message.from_user.id]:
            users[message.from_user.id]['username'] = users[message.from_user.id]['username']
        else:
            users[message.from_user.id]['username'] = message.from_user.username
        if 'iscourier' in  users[message.from_user.id]:
            users[message.from_user.id]['iscourier'] = users[message.from_user.id]['iscourier']
        else:
            users[message.from_user.id]['iscourier'] = False
    else:
        users[message.from_user.id] = users[message.from_user.id]
    markup = types.ReplyKeyboardRemove(selective=False)
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('📪 Отправить посылку')
    if message.from_user.id in courier_users:
        for key in courier_users[message.from_user.id]:
            if courier_users[message.from_user.id][key] == None and key != 'Маршруты':
                itembtn2 = types.KeyboardButton('❌ Режим курьера')
            else:
                if key != 'Маршруты':
                    itembtn2 = types.KeyboardButton('✅ Режим курьера')
        markup.add(itembtn1, itembtn2)
    else:
        itembtn2 = types.KeyboardButton('❌ Режим курьера')
        markup.add(itembtn1, itembtn2)
    bot.reply_to(message, "Добро пожаловать в сервис по отправке посылок!", reply_markup=markup)

@bot.message_handler(func=lambda msg: 'Режим курьера' in msg.text or 'Вернуться' in msg.text)
def courier_mode(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    markup = types.ReplyKeyboardMarkup(row_width=2)
    if message.from_user.id not in courier_users:
        courier_users[message.from_user.id] = new_courier
        async def keybuttons_generate():
            for key in courier_users[message.from_user.id]:
                if courier_users[message.from_user.id][key] == None and key != 'Маршруты':
                    if key == 'Номер телефона':
                        itembtn = types.KeyboardButton('❌ ' + key)
                        markup.add(itembtn)
                    else:
                        itembtn = types.KeyboardButton('❌ ' + key)
                        markup.add(itembtn)
                else:
                    if key != 'Маршруты':
                        itembtn = types.KeyboardButton('✅ ' + key)
                        markup.add(itembtn)
        async def routebuttons_generate():
            await asyncio.gather(keybuttons_generate())
            itembtn1 = types.KeyboardButton('🌎 Маршруты')
            markup.add(itembtn1)
            itembtn2 = types.KeyboardButton('⬅️ Назад')
            markup.add(itembtn2)
            bot.reply_to(message, 'Заполните, пожалуйста, личные данные, чтобы перейти в режим курьера', reply_markup=markup)
        asyncio.run(routebuttons_generate())
    else:
        async def keybuttons_generate():
            for key in courier_users[message.from_user.id]:
                if courier_users[message.from_user.id][key] == None and key != 'Маршруты':
                    if key == 'Номер телефона':
                        itembtn = types.KeyboardButton('❌ ' + key)
                        markup.add(itembtn)
                    else:
                        itembtn = types.KeyboardButton('❌ ' + key)
                        markup.add(itembtn)
                else:
                    if key != 'Маршруты':
                        itembtn = types.KeyboardButton('✅ ' + key)
                        markup.add(itembtn)
        async def routebuttons_generate():
            await asyncio.gather(keybuttons_generate())
            itembtn1 = types.KeyboardButton('🌎 Маршруты')
            markup.add(itembtn1)
            itembtn2 = types.KeyboardButton('⬅️ Назад')
            markup.add(itembtn2)
            bot.reply_to(message, 'Вы хотите внести изменения в личные данные?', reply_markup=markup)
        asyncio.run(routebuttons_generate())

@bot.message_handler(func=lambda msg: 'Номер телефона' in msg.text)
def getNumber(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    itembtn1 = types.KeyboardButton('☎️ Отправить контакт', request_contact=True)
    itembtn2 = types.KeyboardButton('⬅️ Вернуться')
    markup = types.ReplyKeyboardMarkup(row_width=2)
    markup.add(itembtn1, itembtn2)
    bot.reply_to(message, 'Вы можете также отправить номер телефона в виде: "Номер: +______"', reply_markup=markup)

@bot.message_handler(func=lambda msg: 'Номер:' in msg.text)
def number_handler(message):
    new_message = message.text.split('Номер: ')
    for key in courier_users:
        if courier_users[key] == courier_users[message.from_user.id]:
            courier_users[message.from_user.id]['Номер телефона'] = new_message[1]
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.reply_to(message, 'Ваш номер телефона сохранён в системе!', reply_markup=markup)
    courier_mode(message)

@bot.message_handler(content_types=['contact'])
def contact_handler(message):
    for key in courier_users:
        if courier_users[key] == courier_users[message.from_user.id]:
            courier_users[message.from_user.id]['Номер телефона'] = message.contact.phone_number
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.reply_to(message, 'Ваш номер телефона сохранён в системе!', reply_markup=markup)
    courier_mode(message)

@bot.message_handler(func=lambda msg: 'ФИО:' in msg.text)
def update_name(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    new_message = message.text.split('ФИО: ')
    for key in courier_users:
        if courier_users[key] == courier_users[message.from_user.id]:
            courier_users[message.from_user.id]['ФИО'] = new_message[1]
    bot.reply_to(message, "Ваши Ф.И.О сохранены в системе!", reply_markup=markup)
    courier_mode(message)

@bot.message_handler(func=lambda msg: 'ФИО' in msg.text)
def add_name(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    markup = types.ReplyKeyboardMarkup(row_width=2)
    if courier_users[message.from_user.id]['ФИО'] != None:
        itembtn = types.KeyboardButton('⬅️ Вернуться')
        markup.add(itembtn)
        bot.reply_to(message, "Отправьте, пожалуйста, свои Ф.И.О в виде: ФИО: ___ ___ ___", reply_markup=markup)
    else:
        itembtn = types.KeyboardButton('⬅️ Вернуться')
        markup.add(itembtn)
        bot.reply_to(message, "Если вы хотите изменить свои Ф.И.О, отправьте их, пожалуйста, в виде: \"ФИО: ___ ___ ___\"", reply_markup=markup)

@bot.message_handler(func=lambda msg: 'Маршруты' in msg.text)
def getNumber(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    x = 1
    for key in courier_users[message.from_user.id]['Маршруты']:
        bot.send_message(message.chat.id, 'Маршрут ' + str(x))
        for i in range(len(key)):
            bot.send_location(message.chat.id, key[i][0], key[i][1])
        x+=1
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('Маршрут 1')
    itembtn2 = types.KeyboardButton('Маршрут 2')
    itembtn3 = types.KeyboardButton('⬅️ Вернуться')
    markup.add(itembtn1, itembtn2, itembtn3)
    bot.reply_to(message, "Вы хотите изменить свои маршруты?", reply_markup=markup)


@bot.message_handler(func=lambda msg: 'Отправить посылку' in msg.text)
def send_shipment(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    

@bot.message_handler(content_types=["location"])
def function_name(message):
    print(message.location)
    bot.reply_to(message, 'Thank you!')


# calendar

@bot.message_handler(commands='calendar')
def calendar_command_handler(message: types.Message):
    now = date.today()
    bot.send_message(message.chat.id, 'Calendar', reply_markup=generate_calendar_days(year=now.year, month=now.month))


@bot.callback_query_handler(func=None, calendar_config=calendar_factory.filter())
def calendar_action_handler(call: types.CallbackQuery):
    callback_data: dict = calendar_factory.parse(callback_data=call.data)
    year, month = int(callback_data['year']), int(callback_data['month'])
    logging.ingo('calandar: %n, %n', year, month)

    bot.edit_message_reply_markup(call.message.chat.id, call.message.id,
                                  reply_markup=generate_calendar_days(year=year, month=month))


@bot.callback_query_handler(func=None, calendar_zoom_config=calendar_zoom.filter())
def calendar_zoom_out_handler(call: types.CallbackQuery):
    callback_data: dict = calendar_zoom.parse(callback_data=call.data)
    year = int(callback_data.get('year'))

    bot.edit_message_reply_markup(call.message.chat.id, call.message.id,
                                  reply_markup=generate_calendar_months(year=year))


@bot.callback_query_handler(func=lambda call: call.data == EMTPY_FIELD)
def callback_empty_field_handler(call: types.CallbackQuery):
    bot.answer_callback_query(call.id)

bot.infinity_polling()