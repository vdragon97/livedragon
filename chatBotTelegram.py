import telegram
from telegram import ParseMode

def send_test_message(inputMessage):
    try:
        telegram_notify = telegram.Bot("5481822840:AAE1vS9H6fZXsFfsRAKqYjbTGbS-l-gMUTk")
        #Shark Combat 1705730750
        telegram_notify.send_message(chat_id="-1001705730750", text=inputMessage, parse_mode=ParseMode.HTML)
        #Deceitful Candle 1400996369
        #telegram_notify.send_message(chat_id="-1001400996369", text=inputMessage, parse_mode=ParseMode.HTML)
        print("-----chatBotTelegram send sms to Deceitful Candle Channel successfully-----")
    except Exception as ex:
        print(ex)
        print("---------------------------chatBotTelegram error---------------------------")

#send_test_message("Hello there!!!")