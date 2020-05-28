from telegram.ext import Updater
from telegram import Poll, Bot, PollOption, User
import os
#import telepot
import random
#import telebot
import pandas as pd
from flask import Flask, request 
from properties.p import Property
from datetime import datetime
from threading import Lock, Thread
lock = Lock()


lock = Lock()


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
    
    if username in open('blocked_user.txt', encoding = 'utf8').read():
        update.message.reply_text(text="You cant any more")
        return 0
    user.clear()
    reply_markup = InlineKeyboardMarkup(keyboard)
    ids = data2['tweet_id']
    
    lock.acquire()
    if(len(ids) == len(tweet_id)):
        message = 'ሁሉም ዳታ ተሞልቷል በቀጣይ ተጨማሪ ሲኖር እናሳውቆታለን፤ እናመሰግናለን!!'
        update.message.reply_text(message) 
        return 0


    else:
        for x in tweet_id:
            if x not in ids:
                if username in user_tweet_ids and user_tweet_ids[username] != None:
                    break
                else:
                    if x not in [user_tweet_id for user_tweet_id in user_tweet_ids.values()]:
                        user_tweet_ids[username] = x
                        break
    update.message.reply_text(map[user_tweet_ids[username]], reply_markup=reply_markup)
  

    lock.release()
       
    

import csv

def verify(username):
    data1 = pd.read_csv("test_correct_file.csv", encoding= 'utf8',  usecols=['tweet','class'])
    data2 = pd.read_csv("correct_result.csv", encoding= 'utf8', usecols=['text','answer','username'])

    if not os.path.exists('blocked_user.txt'):
        f = open('ids.txt', 'w', encoding='utf8')
        f.close()

    count  = 0
    uname = 'Hizab'

    index0 = data2[data2['username'] == uname].index.values
    if len(index0)>2:
        for x in range(len(index0)-4, len(index0)):
            i = index0[x]
            text = data2['text'][index0[x]]

            index1 = data1[data1['tweet']==text].index.values
            index2 = data2[data2['text']==text].index.values

            r1 = data1['class'][index1[0]] 
            r2 = data2['answer'][index2[0]]
            if(r1 == r2):
                continue
            else:
                count = count + 1
        if count==3:
            message = 'warning'
        elif count==4:
            message = 'block'
            with open('blocked_user.txt', 'a', encoding='utf8') as f:
                f.write(username)
        return message 
def prise(num):

    f = open('5birr.txt', 'r',encoding='utf8')
    five = f.readlines()
    fiv = []
    for x in five:
        j = x.replace(' ','')
        fiv.append(j.rstrip('\n'))


    fil = open('recharge.txt', 'r',encoding='utf8')
    recharge = fil.readlines()
    re = []
    for x in recharge:
        j = x.replace(' ','')
        re.append(j.rstrip('\n'))



    f2 = open('10birr.txt', 'r', encoding='utf8')
    ten = f2.readlines()
    te = []
    for x in ten:
        j = x.replace(' ','')
        te.append(j.rstrip('\n'))



    c = 0
    co = 0

    number = ''

    while (num>0):
        if num==5:
            fil = open('recharge.txt', 'r',encoding='utf8')
            recharge = fil.readlines()
            re = []
            for x in recharge:
                j = x.replace(' ','')
                re.append(j.rstrip('\n'))
            num = num - 5
            for n in fiv:
                if str(n) not in re:
                    number = number + ' ' + n
                    fil = open('recharge.txt', 'a',encoding='utf8')
                    fil.writelines('\n' + n)
                    fil.close()
                    break

        elif num>=10:
            fil = open('recharge.txt', 'r',encoding='utf8')
            recharge = fil.readlines()
            re = []
            for x in recharge:
                j = x.replace(' ','')
                re.append(j.rstrip('\n'))
            for n in te:
                if str(n)  not in re:
                    print(n)
                    number = number + ' ' + n
                    fil = open('recharge.txt', 'a',encoding='utf8')
                    fil.writelines('\n' + str(n))
                    fil.close()
                    break
            num = num - 10
            
            
    return number

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





    if(int(coun) > 526):
        query.edit_message_text(text="ሁሉም ዳታ ተሞልቷል እስካሁን የሞሉት ዳታ ተመዝግቦ ተቀምጧል፣ በቀጣይ ዳታ ብቅርብ ጊዜ እንለቃለን፣ ተመልሰው ይሞክሩ!!")
        return 0
    
    if(int(coun) == 25):
        query.edit_message_text(text="አንኳን ደስ አሎት የ10 ብር ካርድ አሸናፊ ለመሆን የሚያበቃዎትን ግማሽ  ይህል ዳታ አስገብተዋል፣ እባክዎ ለመሸለም ተጨማሪ ዳታ ይሙሉ::")
        #write(query,username)
        #return 0
    if(int(coun) == 50):
        pr = prise(10)
        query.edit_message_text(text=pr)
        write(query,username)
        return 0
    if(int(coun) == 150):
        pr = prise(15)
        query.edit_message_text(text=pr)
        write(query,username)
        return 0
    if(int(coun) == 275):
        pr = prise(15)
        query.edit_message_text(text=pr)
        write(query,username)
        return 0
    if(int(coun) == 525):
        pr = prise(15)
        query.edit_message_text(text=pr)
        write(query,username)
        return 0
    if(int(coun) == 1025):
        pr = prise(15)
        query.edit_message_text(text=pr)
        write(query,username)
        return 0
    if(int(coun) == 2025):
        pr = prise(15)
        query.edit_message_text(text=pr)
        write(query,username)
        return 0
    if(int(coun) == 4025):
        pr = prise(15)
        query.edit_message_text(text=pr)
        write(query,username)
        return 0

       
    write(query,username)
    data2 = pd.read_csv('test_result.csv', encoding='utf8')
    ids = data2['tweet_id']
    if(len(ids) == len(tweet_id)):
        message = 'ሁሉም ዳታ ተሞልቷል እስካሁን የሞሉት ዳታ ተመዝግቦ ተቀምጧል፣ በቀጣይ ዳታ በቅርብ ጊዜ እንለቃለን፣ ተመልሰው ይሞክሩ!!'
        query.edit_message_text(text=message)
        return 0
    else:
        for x in tweet_id:
            if x not in ids:
                if user_tweet_ids[username]:
                    break
                elif x not in [user_tweet_id for user_tweet_id in user_tweet_ids.values()]:
                    user_tweet_ids[username] = x
                    eval(query, x ,map[user_tweet_ids[username]], username)
                    break
      
    if val == 0:
        message = verify(username)  
        if message == 'warning':
            query.edit_message_text(text="ተደጋጋሚ ስህተት እየሰሩ ነው፤ ባክዎን ተጠንቅቀው ይሙሉ")
        elif message == 'block':
            query.edit_message_text(text="ተደጋጋሚ ስህተት ስለ ሰሩ አካውንቶ ታግዶአል፡፡")
            return 0
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

def eval(query,tweet_id,tweet,username):
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=tweet)
    query.edit_message_reply_markup(reply_markup=reply_markup)

def real_control():
    import random
    f = open('correct.txt', encoding='utf8')
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

