import telebot
import os
import pathlib
import phonenumbers

from telebot import types
from dotenv import load_dotenv
from store.models import Posy, Florist, Courier, Client

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'TG BOT'

    def handle(self, *args, **kwargs):
        bot.enable_save_next_step_handlers(delay=2)
        bot.load_next_step_handlers()
        bot.infinity_polling()


load_dotenv()
access_token = os.environ['TG_API_KEY']
bot = telebot.TeleBot(access_token)


def ready_made_posys():
    ready_posys = {}
    for num, posy in enumerate(Posy.objects.order_by('id')[:5]):
        ready_posys[num+1] = {
            "title": posy.title,
            "picture": posy.picture,
            "description": posy.description,
            "price": posy.price,
        }
    return ready_posys


def send_image(bot, call, pic_number):
    script_path = pathlib.Path.cwd()
    file_path = script_path.joinpath(f'flowershop/media/posy_{pic_number}.jpg')
    with open(file_path, 'rb') as posting_file:
        bot.send_photo(chat_id=call.message.chat.id, photo=posting_file)


@bot.message_handler(commands=['start'])
def start(message):
    message_to_customer = f'<b>{message.from_user.first_name}</b>, к какому событию готовитесь? Выберите один из вариантов, либо укажите свой'
    markup = types.InlineKeyboardMarkup()
    bday_button = types.InlineKeyboardButton('День рождения', callback_data= 'occ_birthday')
    wedding_button = types.InlineKeyboardButton('Свадьба', callback_data= 'occ_wedding')
    school_button = types.InlineKeyboardButton('Школа', callback_data= 'occ_school')
    other_occation_button = types.InlineKeyboardButton('Другой повод', callback_data= 'occ_other')
    markup.add(bday_button, wedding_button, school_button, other_occation_button)
    bot.send_message(message.chat.id, message_to_customer, 
                      parse_mode='html', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('occ'))
def handle_occation(call):
    prices = [
        '~500', '~1000', '~2000', 'больше', 'не важно'
        ]
    if call.data == 'occ_birthday':
        markup = types.InlineKeyboardMarkup(row_width=3)
        for price in prices:
            markup.add(types.InlineKeyboardButton(f'{price}', callback_data=f'price {price}'))
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
    if call.data == 'price ~500':
        posy = Posy.objects.get(id=1)
        pic_number = posy.id
        real_price = posy.price
        send_image(bot, call, pic_number)
        message = bot.send_message(call.message.chat.id, f'Ваш букет, стоимостью {real_price}', parse_mode='html', reply_markup=markup)
        bot.register_next_step_handler(message, handle_bouquet)
    elif call.data == 'price ~1000':
        posy = Posy.objects.get(id=2)
        pic_number = posy.id
        real_price = posy.price
        send_image(bot, call, pic_number)
        message = bot.send_message(call.message.chat.id, f'Ваш букет, стоимостью {real_price}', parse_mode='html', reply_markup=markup)
        bot.register_next_step_handler(message, handle_bouquet)
    elif call.data == 'price ~2000':
        posy = Posy.objects.get(id=3)
        pic_number = posy.id
        real_price = posy.price
        send_image(bot, call, pic_number)
        message =bot.send_message(call.message.chat.id, f'Ваш букет, стоимостью {real_price}', parse_mode='html', reply_markup=markup)
        bot.register_next_step_handler(message, handle_bouquet)
    elif call.data == 'price больше':
        posy = Posy.objects.get(id=4)
        pic_number = posy.id
        real_price = posy.price
        send_image(bot, call, pic_number)
        message = bot.send_message(call.message.chat.id, f'Ваш букет, стоимостью {real_price}', parse_mode='html', reply_markup=markup)
        bot.register_next_step_handler(message, handle_bouquet)
    elif call.data == 'price не важно':
        posy = Posy.objects.get(id=5)
        pic_number = posy.id
        real_price = posy.price
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
        message_to_customer = 'Хотите что-то еще более уникальное? Подберите другой букет из нашей коллекции или закажите консультацию флориста.'
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
    message = bot.send_message(message.chat.id, f'Спасибо за Ваш заказ. Если хотиете сделать друго, напишите сообщение: "/start" ',
                               parse_mode='html')
    bot.register_next_step_handler(message, start)


@bot.callback_query_handler(func=lambda call: call.data.startswith('fin'))
def handle_not_aproach(call):
    if call.data == 'fin_consultation':
        message_to_customer = 'Укажите номер телефона, и наш флорист перезвонит Вам в течение 20 минут.'
        message = bot.send_message(call.message.chat.id, message_to_customer, parse_mode='html')
        bot.register_next_step_handler(message, handle_user_phone_number)
    elif call.data == 'fin_collection':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
        bot.send_message(call.message.chat.id, 'Готовые букеты для вас:')
        for key, value in ready_made_posys().items():
            script_path = pathlib.Path.cwd()
            file_path = script_path.joinpath(f'flowershop/media/{value["picture"]}')
            with open(file_path, 'rb') as posting_file:
                bot.send_photo(
                    call.message.chat.id,
                    photo=posting_file,
                    caption=f"{key}. {value['title']} \nЦена: {str(value['price'])} руб."
                )
                markup.add(types.KeyboardButton(text=f'{key}'))
        message = bot.send_message(call.message.chat.id, 'Какой из предложенных будетов Вас интересует?', reply_markup=markup)
        bot.register_next_step_handler(message, handle_user_choise)
    elif call.data == 'fin_cancel':
        message = bot.send_message(call.message.chat.id, 'Если хотите выбрать другой букет, напишите сообщение "/start".')
        bot.register_next_step_handler(message, start)


@bot.message_handler(content_types=['text'])
def handle_user_choise(message):
    choises = set('12345')
    if any((choise in choises) for choise in message.text):
        script_path = pathlib.Path.cwd()
        file_path = script_path.joinpath(f'flowershop/media/posy_{message.text}.jpg')
        with open(file_path, 'rb') as posting_file:
            bot.send_photo(chat_id=message.chat.id, photo=posting_file)
        message = bot.send_message(message.chat.id, 'Ваш букет. Если хотите выбрать другой букет, напишите сообщение "/start"',
                         parse_mode='html')
        bot.register_next_step_handler(message, start)


@bot.message_handler(content_types=['text'])
def handle_user_phone_number(message):
    my_string_number = message.text
    try:
        my_number = phonenumbers.parse(my_string_number)
    except Exception as Err:
        message = bot.send_message(message.chat.id,
                                   f'Введен некорректный номер телефона. Попробуйте еще раз. {Err}',
                                   parse_mode='html')
        bot.register_next_step_handler(message, handle_user_phone_number)
    if phonenumbers.is_valid_number(my_number):
        message = bot.send_message(message.chat.id,
                                   f'Спасибо за ваш отклик. Для возврата в начальное меню нажмите: "/start" ',
                                   parse_mode='html')
        bot.register_next_step_handler(message, start)
    else:
        message = bot.send_message(message.chat.id,
                                   f'Введен некорректный номер телефона. Попробуйте еще раз',
                                   parse_mode='html')
        bot.register_next_step_handler(message, handle_user_phone_number)


if __name__ == "__main__":
    bot.polling(non_stop=True)
