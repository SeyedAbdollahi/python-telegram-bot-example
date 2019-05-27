import logging
import os
import WebScripts
import json
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import ReplyKeyboardMarkup
import jdatetime
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import sys
sys.path.insert(0, './Database')
import database

# read config.json file
def read_config():
    with open('config.json') as jsonFile:
        return json.load(jsonFile)

# get config data
config = read_config()

# add data to events.log file
def add_event_log(action, user):
    log = 'Action: [%s], link: [%s], full_name: [%s]' % (action, user.link, user.full_name)
    database.insert_log(log)

# /log : get data from postgresql database and send events.log file
def send_log(bot, update):
    if update.message.from_user.id in config['bot']['admin']:
        try:
            logs = database.get_logs()
            if len(logs) > 0:
                with open('./events.log', 'w') as log_file:
                    log_file.write(logs)
                bot.send_document(chat_id=update.message.chat_id, document=open('events.log', 'rb'))
                os.remove('./events.log')
            else:
                bot.send_message(chat_id=update.message.chat_id, text='events.log is empty!')
        except(Exception) as error:
            print('error in get_logs from database:', error)
    else:
        bot.send_message(chat_id=update.message.chat_id, text='access denied')
    add_event_log('/log', update.message.from_user)

# /delete_logs: delete all logs from postgresql database
def delete_logs(bot, update):
    if update.message.from_user.id in config['bot']['admin']:
        send_log(bot, update)
        database.delete_logs()
        bot.send_message(chat_id=update.message.chat_id, text='all logs deleted!')
    else:
        bot.send_message(chat_id=update.message.chat_id, text='access denied')
    add_event_log('/delete_logs', update.message.from_user)

# /database: send database.json file
def send_database(bot, update):
    if update.message.from_user.id in config['bot']['admin']:
        bot.send_document(chat_id=update.message.chat_id, document=open('./Database/database.json', 'rb'))
    else:
        bot.send_message(chat_id=update.message.chat_id, text='access denied')
    add_event_log('/database', update.message.from_user)

# /start
def start(bot, update):
    welcome_text = "🤖 سلام! \n به ربات قیمت یاب خوش آمدید. \n در حال حاضر من می توانم قیمت لحظه ای طلای 18 عیار ، طلای 24 عیار و انس طلا را نمایش بدهم."
    bot.send_message(chat_id=update.effective_message.chat_id, text=welcome_text)
    add_event_log('/start', update.message.from_user)

# /gold18k
def gold18k(bot, update):
    update.effective_message.reply_text('در حال بررسی قیمت طلا 18 عیار')
    update.effective_message.reply_text(WebScripts.gold_scripts('gold18k'))
    add_event_log('/gold18k', update.message.from_user)

# /gold24k
def gold24k(bot, update):
    update.effective_message.reply_text('در حال بررسی قیمت طلا 24 عیار')
    update.effective_message.reply_text(WebScripts.gold_scripts('gold24k'))
    add_event_log('/gold24k', update.message.from_user)

# /gold_ons
def gold_ons(bot, update):
    update.effective_message.reply_text('در حال بررسی قیمت انس طلا')
    update.effective_message.reply_text(WebScripts.gold_scripts('gold_ons'))
    add_event_log('/gold_ons', update.message.from_user)

def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)

# /version
def version(bot, update):
    bot.send_message(update.effective_message.chat_id, text=config['app']['version'])
    add_event_log('/version', update.message.from_user)

if __name__ == "__main__":
    # Set these variable to the appropriate values
    TOKEN = config['bot']['token']

    # Enable logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Set up the Updater
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    # Add handlers
    #   Main Command (all-users)
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('gold18k', gold18k))
    dp.add_handler(CommandHandler('gold24k', gold24k))
    dp.add_handler(CommandHandler('gold_ons', gold_ons))
    #   Sub Command (all-users)
    dp.add_handler(CommandHandler('version', version))
    #   System Command (admin)
    dp.add_handler(CommandHandler('log', send_log))
    dp.add_handler(CommandHandler('delete_logs', delete_logs))
    dp.add_handler(CommandHandler('database', send_database))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()
