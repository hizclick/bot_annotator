from telegram.ext import Updater
from telegram import Poll, Bot, PollOption, User
import os
import telepot
import random
#import telebot
import pandas as pd
from flask import Flask, request 
from properties.p import Property
from datetime import datetime

user_real = {}
prop = Property()

bot_prop = prop.load_property_files('bot.properties')

if not os.path.exists('test_result.csv'):
    columns = ['tweet_id','sentiment','username']
    df = pd.DataFrame(columns=columns)
    df.to_csv('test_result.csv', index = False)


if not os.path.exists('correct_result.csv'):
    columns = ['text','answer','username']
    df = pd.DataFrame(columns=columns)
    df.to_csv('test_correct_result.csv', index = False)

if not os.path.exists('ids.txt'):
    f = open('ids.txt', 'w', encoding='utf8')
    f.close()
data = pd.read_csv('test_annotation.csv', encoding='utf8')
data2 = pd.read_csv('test_result.csv', encoding='utf8')

tweet_id2 = data2['tweet_id']
sentiment = data2['sentiment']

count = data2['username'].value_counts()

server= Flask(__name__)


tweet_id = data['tweet_id']


tweet = data['tweet']
user = []

user_tweet_ids = {} #username1 = tweet_id1, username2 = tweet_id2

map = dict()
map2 = dict()
for item in tweet_id.keys():

    map[tweet_id[item]] = tweet[item]

for item in tweet_id2.keys():
    map2[tweet_id2[item]] = sentiment[item]


 # converting to dict 
  
# display 


#bot = telebot.TeleBot(token = TOKEN)
TOKEN = bot_prop['TOKEN']

import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

text = dict()

keyboard = [[InlineKeyboardButton("ገንቢ", callback_data='Pos'),
                 InlineKeyboardButton("አፍራሽ", callback_data='Neg'),
                 InlineKeyboardButton("ገለልተኛ", callback_data='Nuet'),
                 InlineKeyboardButton("ቅልቅል", callback_data='Mix')]]

def start(update, context):
    data2 = pd.read_csv('test_result.csv', encoding='utf8')
    username = update.effective_user.username
    if username == None:
        update.message.reply_text(text="እባክዎን በመጀመሪያ ዩዘርኔም ሴቲንግ ውስጥ ገብተው ይፍጠሩ:: Settings-->Edit Profile-->Add username--Save")
        return 0
    #f   = open('ids.txt', 'r', encoding='utf8')
    #ids = f.read().strip().split("\n")
    reply_markup = InlineKeyboardMarkup(keyboard)
    ids = data2['tweet_id']
    
       
    if(len(ids) == len(tweet_id)):
        message = 'ሁሉም ዳታ ተሞልቷል በቀጣይ ተጨማሪ ሲኖር እናሳውቆታለን፤ እናመሰግናለን!!'
        update.message.reply_text(message) 
        return 0


    else:
        for x in tweet_id:
            print(user_tweet_ids[username])
            if user_tweet_ids[username]:
                 break
            if x not in tweet_id2 and x not in [user_tweet_id for user_tweet_id in user_tweet_ids.values()]:
                user_tweet_ids[username] = x
                break
    update.message.reply_text(map[user_tweet_ids[username]], reply_markup=reply_markup)
  


import csv

def button(update, context):
    data2 = pd.read_csv('test_result.csv', encoding='utf8')
    query = update.callback_query
    username = update.effective_user.username
    if username == None:
        query.edit_message_text(text="እባክዎን በመጀመሪያ ዩዘርኔም ሴቲንግ ውስጥ ገብተው ይፍጠሩ::Settings-->Edit Profile-->Add username--Save")
        return 0
    user.clear()

    
    #f   = open('ids.txt', 'r', encoding='utf8')
    #ids = f.read().strip().split("\n")

    ids = data2['tweet_id']
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    user.clear()
    for x in data2['username']:
        user.append(x) 
    coun = user.count(username) 
    val = coun %6
    print(val)

    if(int(coun) > 526):
        query.edit_message_text(text="ሁሉም ዳታ ተሞልቷል እስካሁን የሞሉት ዳታ ተመዝግቦ ተቀምጧል፣ በቀጣይ ዳታ ብቅርብ ጊዜ እንለቃለን፣ ተመልሰው ይሞክሩ!!")
        return 0
    
    if(int(coun) == 25):
        query.edit_message_text(text="አንኳን ደስ አሎት የ10 ብር ካርድ አሸናፊ ለመሆን የሚያበቃዎትን ግማሽ  ይህል ዳታ አስገብተዋል፣ እባክዎ ለመሸለም ተጨማሪ ዳታ ይሙሉ::")
        #write(query,username)
        #return 0
    if(int(coun) == 50):
        query.edit_message_text(text="አንኳን ደስ አሎት የ10 ብር ካርድ አሸናፊ ለመሆን የሚያበቃዎትን ይህል ዳታ አስገብተዋል የሞሉትን መረጃ ትክክለኛነት አረጋግጠን በእለቱ መጨረሻ የካርድ ቁጥሩን እንልክሎታለን ፤ ለመቀጠል '/start' የሚለውን ይጫኑ")
        write(query,username)
        return 0
    if(int(coun) == 150):
        query.edit_message_text(text="አንኳን ደስ አሎት ተጨማሪ የ15 ብር ካርድ አሸናፊ ለመሆን የሚያበቃዎትን ይህል ዳታ አስገብተዋል የሞሉትን መረጃ ትክክለኛነት አረጋግጠን በእለቱ መጨረሻ የካርድ ቁጥሩን እንልክሎታለን ፤ ለመቀጠል '/start' የሚለውን ይጫኑ")
        write(query,username)
        return 0
    if(int(coun) == 275):
        query.edit_message_text(text="አንኳን ደስ አሎት ተጨማሪ የ25 ብር ካርድ አሸናፊ ለመሆን የሚያበቃዎትን ይህል ዳታ አስገብተዋል የሞሉትን መረጃ ትክክለኛነት አረጋግጠን በእለቱ መጨረሻ የካርድ ቁጥሩን እንልክሎታለን ፤ ለመቀጠል '/start' የሚለውን ይጫኑ")
        write(query,username)
        return 0
    if(int(coun) == 525):
        query.edit_message_text(text="አንኳን ደስ አሎት ተጨማሪ የ50 ብር ካርድ አሸናፊ ለመሆን የሚያበቃዎትን ይህል ዳታ አስገብተዋል የሞሉትን መረጃ ትክክለኛነት አረጋግጠን በእለቱ መጨረሻ የካርድ ቁጥሩን እንልክሎታለን ፤ ለመቀጠል '/start' የሚለውን ይጫኑ")
        write(query,username)
        return 0
    if(int(coun) == 1025):
        query.edit_message_text(text="አንኳን ደስ አሎት ተጨማሪ የ100 ብር ካርድ አሸናፊ ለመሆን የሚያበቃዎትን ይህል ዳታ አስገብተዋል የሞሉትን መረጃ ትክክለኛነት አረጋግጠን በእለቱ መጨረሻ የካርድ ቁጥሩን እንልክሎታለን ፤ ለመቀጠል '/start' የሚለውን ይጫኑ")
        write(query,username)
        return 0
    if(int(coun) == 2025):
        query.edit_message_text(text="አንኳን ደስ አሎት ተጨማሪ የ200 ብር ካርድ አሸናፊ ለመሆን የሚያበቃዎትን ይህል ዳታ አስገብተዋል የሞሉትን መረጃ ትክክለኛነት አረጋግጠን በእለቱ መጨረሻ የካርድ ቁጥሩን እንልክሎታለን ፤ ለመቀጠል '/start' የሚለውን ይጫኑ")
        write(query,username)
        return 0
    if(int(coun) == 4025):
        query.edit_message_text(text="አንኳን ደስ አሎት ተጨማሪ የ400 ብር ካርድ አሸናፊ ሆነዋል ለመሆን የሚያበቃዎትን ይህል ዳታ አስገብተዋል የሞሉትን መረጃ ትክክለኛነት አረጋግጠን በእለቱ መጨረሻ የካርድ ቁጥሩን እንልክሎታለን ፤ ለመቀጠል '/start' የሚለውን ይጫኑ")
        write(query,username)
        return 0

       
    write(query,username)
    if(len(ids) == len(tweet_id)):
        message = 'ሁሉም ዳታ ተሞልቷል እስካሁን የሞሉት ዳታ ተመዝግቦ ተቀምጧል፣ በቀጣይ ዳታ ብቅርብ ጊዜ እንለቃለን፣ ተመልሰው ይሞክሩ!!'
        query.edit_message_text(text=message)
        return 0
    else:
        for x in tweet_id:
            if user_tweet_ids[username]:
                break
            if x not in tweet_id2 and x not in [user_tweet_id for user_tweet_id in user_tweet_ids.values()]:
                user_tweet_ids[username] = x
                eval(query, user_tweet_ids[username] ,map[user_tweet_ids[username]])
                break
      
    if val == 0:
        reply_markup = InlineKeyboardMarkup(keyboard)
        user_real[username]  = real_control()
        query.edit_message_text(text=user_real[username])
        query.edit_message_reply_markup(reply_markup=reply_markup)
        write_correct(query,username,user_real[username])

        
def write_correct(query, username, message):
    with open('correct_result.csv', 'a', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow([message,format(query.data),str(username)])
        user_real[username] = None

def eval(query,tweet_id,tweet):
    message = map[tweet_id]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=message)
    query.edit_message_reply_markup(reply_markup=reply_markup)

def real_control():
    import random
    f = open('test_correct.txt', encoding='utf8')
    text = f.readlines()
    fin= []
    for x in text:
        fin.append(x.replace('\n',''))
    return random.choice(fin)

   

def write(query,username):
    print('hihih')
    #for key in text:
    #text[key] = format(query.data)
    #print(text)
    with open('test_result.csv', 'a', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow([user_tweet_ids[username],format(query.data),map[user_tweet_ids[username]],str(username)])
        print([user_tweet_ids[username],format(query.data),map[user_tweet_ids[username]],str(username)])
        user_tweet_ids[username] = None

    

def help(update, context):
    update.message.reply_text("Use /start to test this bot.")

def end(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text='ስለ ትብብርዎ እናመሰግናለን!')

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def instruction(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='ጽሁፉ ገምቢ ከሆነ "ገምቢ" የሚለውን፣ አፍራሽ ከሆነ "አፍራሽ" የሚለውን፣ ገለልትኛ "ገለልተኛ" የሚለውን ፣ የገምቢ እና የአፍራሽ ቅልቅል ከሆነ "ቅልቅል" የሚለውን ይምረጡ፡፡ ይህንን መረጃ ሲሞሉ በትክክል በመለሱት ጥያቄ ልክ በዕለቱ መጨረሻ በእርስዎ "user name" በኩል የሞባይል ካርድ ሽልማት ይላክለዎታል። ለበለጠ መረጃ https://annotation-wq.github.io/')
def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    updater.dispatcher.add_handler(CommandHandler('end', end))
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('instruction', instruction))
    updater.dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()

@server.route("/" + TOKEN, methods = ['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode('utf-8'))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://dataannotatort.com/" + TOKEN)
    return "!", 200


if __name__ == '__main__':
    main()

