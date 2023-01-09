import telebot
from config import keys, TOKEN
from extensions import ConvertationException, Converter


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать, в сообщении через пробел введите сначало исходную валюту, ' \
           '\nзатем валюту в которую хотите перевести и количество переводимой валюты.' \
           '\nЧтобы увидеть список всех доступных валют и их варианты ввода, введите: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные варианты для ввода валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text',])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertationException('Слишком много/мало параметров.')
        quote, base, amount = values
        total_base = Converter.convert(quote, base, amount)
    except ConvertationException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}.')
    else:
        text = f'{amount} {quote} это: {round((float(total_base) * float(amount)),2)} {base}'
        bot.send_message(message.chat.id, text)



bot.polling()