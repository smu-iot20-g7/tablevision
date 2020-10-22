from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from mongoengine import connect, disconnect
from models import *
import os, sys
from datetime import datetime, timedelta
from pymongo import MongoClient

GROUP_CHAT_ID = -446302578
TOKEN = os.environ['TELEGRAM_TOKEN']

# connect("iot", host=os.environ['DB_URI'])

def remind(event, context):
    now = datetime.now() + timedelta(hours=8)
    print("timing now", now)
    bot = Bot(token=TOKEN)
    table_alive = False
    trayin_alive = False
    trayout_alive = False

    # Tablevision
    disconnect()
    connect("iot", host=os.environ['DB_URI'])
    sessions = Session.objects()
    for session in sessions:
        if (now - session.sessionStart).total_seconds() <= 3600:
            table_alive = True
            break

    # Tray in
    disconnect()
    client = MongoClient(os.environ['DB_URI'])
    db = client['fsr_rfid']
    collection = db['tray_in']
    cursor = collection.find({})
    for document in cursor:
        if (now - document['timestamp']).total_seconds() <= 3600:
            print("tray in")
            print(document['timestamp'])
            trayin_alive = True
            break
    
        
    # Tray out
    client.close()
    connect("fsr_rfid", host=os.environ['DB_URI'])
    collections = Collection.objects()
    for collection in collections:
        if (now - collection.timestamp).total_seconds() <= 3600:
            print("tray out")
            print(collection.timestamp)
            trayout_alive = True
            break

        
    text = "<b>Health Check</b> - Team Hardcode\n\nTable Vision: {}\nTray In: {}\nTray Out: {}".format(get_emoji(table_alive), get_emoji(trayin_alive), get_emoji(trayout_alive))
    bot.sendMessage(chat_id=GROUP_CHAT_ID, text=text, parse_mode='html')
    # bot.sendMessage(chat_id=GROUP_CHAT_ID, text="GG guys i think tablevision is broken gndahsdiasuhaiu")

    # bot.sendMessage(chat_id=GROUP_CHAT_ID, text="Tray in is alive sirs, dont worry")
    # bot.sendMessage(chat_id=GROUP_CHAT_ID, text="GG guys i think tablevision is broken gndahsdiasuhaiu")

    # bot.sendMessage(chat_id=GROUP_CHAT_ID, text="Tray out is alive sirs, dont worry")
    # bot.sendMessage(chat_id=GROUP_CHAT_ID, text="GG guys i think trayout is fking ded gndahsdiasuhaiu")

def get_emoji(status):
    if status:
        return u'\U00002705'

    return u'\U0000274c'

if __name__ == '__main__':
    now = datetime.now()
    connect("fsr_rfid", host=os.environ['DB_URI'])
    collections = Collection.objects()
    for collection in collections:
        if (now - collection.timestamp).seconds <= 3600:
            print(collection.timestamp)
            print("A?????")
            # trayout_alive = True
    print("testing")