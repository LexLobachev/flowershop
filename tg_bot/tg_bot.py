import telebot
import os
import pathlib
import phonenumbers
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type
from telebot import types
from dotenv import load_dotenv


load_dotenv()
access_token = os.environ['TG_API_KEY']
bot = telebot.TeleBot(access_token)

def send_image(bot, call, pic_number):
    file_path = f'media/posy_{pic_number}.jpg'
    with open(file_path, 'rb') as posting_file:
        bot.send_photo(chat_id=call.message.chat.id, photo=posting_file)


@bot.message_handler(commands=['start'])
def start(message):
    message_to_customer = f'Здравствуйте, <b>{message.from_user.first_name}</b>! К какому событию хотите подобрать букет? Выберите один из вариантов, либо укажите свой'
    markup = types.InlineKeyboardMarkup()
    bday_button = types.InlineKeyboardButton('День рождения', callback_data= 'occ_birthday')
    wedding_button = types.InlineKeyboardButton('Свадьба', callback_data= 'occ_wedding')
    school_button = types.InlineKeyboardButton('Школа', callback_data= 'occ_school')
    no_occation_button = types.InlineKeyboardButton('Нет повода', callback_data= 'occ_no')
    other_occation_button = types.InlineKeyboardButton('Другой повод', callback_data= 'occ_other')
    markup.add(bday_button, wedding_button, school_button, no_occation_button, other_occation_button)
    bot.send_message(message.chat.id, message_to_customer, 
                      parse_mode='html', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('occ'))
def handle_occation(call):
    prices = [
        '~500 ₽', '~1000 ₽', '~2000 ₽', 'больше', 'не важно'
        ]
    if call.data == 'occ_birthday':
        markup = types.InlineKeyboardMarkup(row_width=3)
        for price in prices:
            markup.add(types.InlineKeyboardButton(f'{price}', parse_mode='html', callback_data=f'price {price}'))
        message = bot.send_message(call.message.chat.id, 'Вы готовитесь ко дню рождения, на какую сумму вы рассчитываете?',
                         parse_mode='html', reply_markup=markup)
    elif call.data == 'occ_wedding':
        markup = types.InlineKeyboardMarkup(row_width=3)
        for price in prices:
            markup.add(types.InlineKeyboardButton(f'{price}', callback_data=f'price {price}'))
        message = bot.send_message(call.message.chat.id, 'Вы готовитесь к свадьбе, на какую сумму вы рассчитываете?',
                         parse_mode='html', reply_markup=markup)
    elif call.data == 'occ_school':
        markup = types.InlineKeyboardMarkup(row_width=3)
        for price in prices:
            markup.add(types.InlineKeyboardButton(f'{price}', callback_data=f'price {price}'))
        message = bot.send_message(call.message.chat.id, 'Вы готовитесь к школе, на какую сумму вы рассчитываете?',
                         parse_mode='html', reply_markup=markup)
    elif call.data == 'occ_no':
        markup = types.InlineKeyboardMarkup(row_width=3)
        for price in prices:
            markup.add(types.InlineKeyboardButton(f'{price}', callback_data=f'price {price}'))
        message = bot.send_message(call.message.chat.id, 'Отсутствие повода - тоже повод! На какую сумму Вы рассчитываете?',
                         parse_mode='html', reply_markup=markup)
    elif call.data == 'occ_other':
        markup = types.InlineKeyboardMarkup(row_width=3)
        message_to_customer = 'Опишите кратко Ваш случай.'
        message = bot.send_message(call.message.chat.id, message_to_customer,
                         parse_mode='html', reply_markup=markup)
        bot.register_next_step_handler(message, handle_other_occation)


@bot.message_handler(content_types=['text'])
def handle_other_occation(message):
    prices = [
        '~500', '~1000', '~2000', 'больше', 'не важно'
    ]
    saved_user_message = message.text
    print(saved_user_message)
    message_to_customer = 'Спасибо за информацию, постараемся подобрать Вам соответствующий букет. Подскажите, на какую сумму Вы рассчитываете?'
    markup = types.InlineKeyboardMarkup(row_width=3)
    for price in prices:
        markup.add(types.InlineKeyboardButton(f'{price}', callback_data=f'price {price}'))
    bot.send_message(message.chat.id, message_to_customer, parse_mode='html', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('price'))
def handle_price(call):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
    order = types.KeyboardButton(text='Заказать букет')
    other = types.KeyboardButton(text='Не подходит')
    markup.add(order, other)
    if call.data == 'price ~500 ₽':
        pic_number = '1'
        real_price = '485'
        send_image(bot, call, pic_number)
        message = bot.send_message(call.message.chat.id, f'Ваш букет, стоимостью {real_price}', parse_mode='html', reply_markup=markup)
        bot.register_next_step_handler(message, handle_bouquet)
    elif call.data == 'price ~1000 ₽':
        pic_number = '2'
        real_price = '867'
        send_image(bot, call, pic_number)
        message = bot.send_message(call.message.chat.id, f'Ваш букет, стоимостью {real_price}', parse_mode='html', reply_markup=markup)
        bot.register_next_step_handler(message, handle_bouquet)
    elif call.data == 'price ~2000 ₽':
        pic_number = '3'
        real_price = '1658'
        send_image(bot, call, pic_number)
        message =bot.send_message(call.message.chat.id, f'Ваш букет, стоимостью {real_price}', parse_mode='html', reply_markup=markup)
        bot.register_next_step_handler(message, handle_bouquet)
    elif call.data == 'price больше':
        pic_number = '4'
        real_price = '2100'
        send_image(bot, call, pic_number)
        message = bot.send_message(call.message.chat.id, f'Ваш букет, стоимостью {real_price}', parse_mode='html', reply_markup=markup)
        bot.register_next_step_handler(message, handle_bouquet)
    elif call.data == 'price не важно':
        pic_number = '5'
        real_price = '2341'
        send_image(bot, call, pic_number)
        message = bot.send_message(call.message.chat.id, f'Ваш букет, стоимостью {real_price}', parse_mode='html', reply_markup=markup)
        bot.register_next_step_handler(message, handle_bouquet)


@bot.message_handler(content_types=['text'])
def handle_bouquet(message):
    if message.text == 'Заказать букет':
        message = bot.send_message(message.chat.id, f'Ваш заказ будет передан курьеру. Напишите ваши данные. Имя:',
                                   parse_mode='html')
        bot.register_next_step_handler(message, handle_user_name)
    elif message.text == 'Не подходит':
        message_to_customer = 'Хотите что-то более уникальное? Подберите другой букет из нашей коллекции или закажите консультацию флориста.'
        markup = types.InlineKeyboardMarkup(row_width=1)
        consultation = types.InlineKeyboardButton(text='Консультация специалиста', callback_data='fin_consultation')
        collection = types.InlineKeyboardButton(text='Посмотреть коллекцию', callback_data='fin_collection')
        cancel = types.InlineKeyboardButton(text='Отменить', callback_data='fin_cancel')
        markup.add(consultation, collection, cancel)
        bot.send_message(message.chat.id, message_to_customer, parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def handle_user_name(message):
    print(message.text)
    message = bot.send_message(message.chat.id, f'Адрес: ',
                               parse_mode='html')
    bot.register_next_step_handler(message, handle_user_adress)


@bot.message_handler(content_types=['text'])
def handle_user_adress(message):
    message = bot.send_message(message.chat.id, f'Желаемое время доставки',
                               parse_mode='html')
    bot.register_next_step_handler(message, handle_user_delivery_time)


@bot.message_handler(content_types=['text'])
def handle_user_delivery_time(message):
    message = bot.send_message(message.chat.id, f'Номер телефона',
                               parse_mode='html')
    bot.register_next_step_handler(message, handle_user_phone)


@bot.message_handler(content_types=['text'])
def handle_user_phone(message):
    try:
        if carrier._is_mobile(number_type(phonenumbers.parse(message.text))) and len(message.text)==12:
            message = bot.send_message(message.chat.id, f'Спасибо за Ваш заказ. Если хотите сделать другой заказ, напишите сообщение: "/start" ',
                                       parse_mode='html')
            bot.register_next_step_handler(message, start)
    except:
        message = bot.send_message(message.chat.id, 'Вами был введен неверный номер, попробуйте ввести через +7')
        bot.register_next_step_handler(message, handle_user_phone)
        pass


@bot.callback_query_handler(func=lambda call: call.data.startswith('fin'))
def handle_not_aproach(call):
    if call.data == 'fin_consultation':
        message_to_customer = 'Укажите номер телефона, и наш флорист перезвонит Вам в течение 20 минут.'
        message = bot.send_message(call.message.chat.id, message_to_customer, parse_mode='html')
        bot.register_next_step_handler(message, handle_user_phone_number)
    elif call.data == 'fin_collection':
        pic_quantity = 5
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
        for pic_number in range(1, pic_quantity+1):
            send_image(bot, call, str(pic_number))
            markup.add(types.KeyboardButton(text=f'{pic_number}'))
        message = bot.send_message(call.message.chat.id, 'Какой из предложенных букетов Вас интересует?', reply_markup=markup)
        bot.register_next_step_handler(message, handle_user_choise)
    elif call.data == 'fin_cancel':
        message = bot.send_message(call.message.chat.id, 'Если хотите выбрать другой букет, напишите сообщение "/start".')
        bot.register_next_step_handler(message, start)


@bot.message_handler(content_types=['text'])
def handle_user_choise(message):
    choises = set('12345')
    if  any((choise in choises) for choise in message.text):
        file_path = f'media/posy_{message.text}.jpg'
        with open(file_path, 'rb') as posting_file:
            bot.send_photo(chat_id=message.chat.id, photo=posting_file)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
        order = types.KeyboardButton(text='Заказать букет')
        other = types.KeyboardButton(text='Не подходит')
        markup.add(order, other)
        message = bot.send_message(message.chat.id, 'Ваш букет',
                         parse_mode='html', reply_markup=markup)
        bot. register_next_step_handler(message, handle_bouquet)


@bot.message_handler(content_types=['text'])
def handle_user_phone_number(message):
    try:
        if carrier._is_mobile(number_type(phonenumbers.parse(message.text))) and len(message.text)==12:
            markup = types.InlineKeyboardMarkup()
            collection_button = types.InlineKeyboardButton(text='Коллеция', callback_data='fin_collection')
            cancel_button = types.InlineKeyboardButton(text='Отменить', callback_data='fin_cancel')
            markup.add(collection_button, cancel_button)
            bot.send_message(message.chat.id, 'Ваш номер был отправлен флористу. Желаете ознакомиться с коллецией, пока ждёте?',
                             reply_markup=markup)
    except phonenumbers.phonenumberutil.NumberParseException:
        message = bot.send_message(message.chat.id, 'Вами был введен неверный номер, попробуйте ввести через +7')
        bot.register_next_step_handler(message, handle_user_phone_number)
        pass


if __name__ == "__main__":
    bot.polling(non_stop=True)
