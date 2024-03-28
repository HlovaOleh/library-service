import telebot
from library_service.settings import TELEGRAM_BOT_TOKEN, CHAT_ID


bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


@bot.message_handler(commands=["start"])
def send_welcome(message: telebot.types.Message) -> None:

    if message.from_user.last_name is None:
        name = f"{message.from_user.first_name}"
    else:
        name = f"{message.from_user.full_name}"

    bot.reply_to(message,
                 f"Hello, {name}!\n"
                 f"Welcome to the Library Service!\n\n"
                 f"/help for more information")


@bot.message_handler(commands=["help"])
def send_help_information(message: telebot.types.Message) -> None:
    bot.reply_to(message,
                 "/start - start bot\n"
                 "/help - show information about commands\n"
                 "/my_borrowings - show all your borrowings\n")


def send_telegram_notification(message):
    bot.send_message(CHAT_ID, text=message)


bot.polling()
