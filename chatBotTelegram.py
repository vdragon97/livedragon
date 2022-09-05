import telegram
import random

def send_test_message(inputMessage):
    try:
        telegram_notify = telegram.Bot("5481822840:AAE1vS9H6fZXsFfsRAKqYjbTGbS-l-gMUTk")
        telegram_notify.send_message(chat_id="-1001400996369", text=inputMessage, parse_mode='Markdown')
        print("-----chatBotTelegram send sms to Deceitful Candle Channel successfully-----")
    except Exception as ex:
        print(ex)
        print("---------------------------chatBotTelegram error---------------------------")

#send_test_message("Hello there!!!")