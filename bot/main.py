import telebot as tb
from telebot import types
import asyncio

bot = tb.TeleBot("", parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN

courier_users = {}

new_courier = {
    'ФИО': None,
    'Номер телефона': None,
    'Маршруты': []
}

@bot.message_handler(func=lambda msg: 'start' in msg.text or 'Назад' in msg.text)
def send_welcome(message):
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
    bot.reply_to(message, "Добро пожаловать в сервис по нахождению посылок! Выберите, пожалуйста, желаемое действие из представленного ниже меню:", reply_markup=markup)

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

@bot.message_handler(func=lambda msg: 'Отправить посылку' in msg.text)
def send_shipment(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.reply_to(message, "Сейчас отправим вашу посылку!", reply_markup=markup)

@bot.message_handler(content_types=["location"])
def function_name(message):
    print(message.location)
    bot.reply_to(message, 'Thank you!')

bot.infinity_polling()