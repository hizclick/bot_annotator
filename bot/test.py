from telegram.ext import Updater
from telegram import Poll, Bot, PollOption, User
import os
import telepot
import random
#import telebot
import pandas as pd
from flask import Flask, request 

data = pd.read_csv('annotation.csv', encoding='utf8')
data2 = pd.read_csv('result.csv', encoding='utf8')

tweet_id2 = data2['tweet_id']
sentiment = data2['sentiment']

count = data2['username'].value_counts()

server= Flask(__name__)

tweet_id = data['tweet_id']
tweet = data['tweet']
user = []



map = dict()
map2 = dict()
for item in tweet_id.keys():

    map[tweet_id[item]] = tweet[item]

for item in tweet_id2.keys():

    map2[tweet_id[item]] = sentiment[item]

 # converting to dict 
  
# display 


TOKEN = '1022567655:AAGjqp1EcNQKQlFlzMIr6MpLQLIoi_YJ4YM'
#bot = telebot.TeleBot(token = TOKEN)

'''
updater = Updater(token=TOKEN, use_context=True)


text = open('test.txt', "r", encoding="utf-8")

lines = text.readlines()

def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


dispatcher = updater.dispatcher
message = list()
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def start(update, context):
    global lines
    global message
    for num, aline in enumerate(lines, 2):
      if random.randrange(num): continue
      lin = aline
    context.bot.send_message(chat_id=update.effective_chat.id, text=lin)
    message.append(lin)


import logging
from telegram.ext import CommandHandler
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def instruction(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='ጽሁፉ አዎንታዊ ከሆነ "1"ን አሉታዊ "2"ን ገለልትኛ ከሆነ "3" ይጻፉ')

import logging
from telegram.ext import CommandHandler
instr = CommandHandler('instruction', instruction)
dispatcher.add_handler(instr)

dispatcher = updater.dispatcher

hi = list()
count = 1

def echo(update, context):
    global lines
    global count 
    
    if(count<len(lines) and len(lines)>0):
        if(update.message.text == '1' or update.message.text == '2' or update.message.text == '3'):
            text = open('test.txt', "r", encoding="utf-8")
            
            lines = text.readlines()

            print('first')
            print(message[0])
            with open('test2.txt', 'a', encoding="utf-8") as f: 
                f.writelines(update.message.text+"," + str(message[0]) + "\n")
            
            
            for num, aline in enumerate(lines, 2):
                if random.randrange(num): continue
                line = aline
            

            message.clear()
            message.append(line)
            context.bot.send_message(chat_id=update.effective_chat.id, text=message[0])

            print("second")
            print(message[0])
            print(message)

        elif(update.message.text == '/end'):
            context.bot.send_message(chat_id=update.effective_chat.id, text='ስለ ትብብሮ እናመሰግናለን!')
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text='እባክዎን ጽሁፉ አዎንታዊ ከሆነ "1"ን አሉታዊ "2"ን ገለልትኛ ከሆነ "3" ይጻፉ')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='ስለ ትብብሮ እናመሰግናለን!')

def end(update,context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='ስለ ትብብሮ እናመሰግናለን!')




from telegram.ext import MessageHandler, Filters
end_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(end_handler)

start_handler = CommandHandler('end', end)
dispatcher.add_handler(start_handler)
updater.start_polling()
'''

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Basic example for a bot that uses inline keyboards.
"""
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

text = dict()

keyboard = [[InlineKeyboardButton("አዎንታዊ", callback_data='Pos'),
                 InlineKeyboardButton("አሉታዊ", callback_data='Neg'),
                 InlineKeyboardButton("ገለልተኛ", callback_data='Nuet'),
                 InlineKeyboardButton("ቅልቅል", callback_data='Mix')]]

def start(update, context):
    text.clear()
   

    reply_markup = InlineKeyboardMarkup(keyboard)

    tweet_id, tweet = random.choice(list(map.items()))
    
    if tweet_id not in map2:
        text[tweet_id] = tweet

    message = tweet
    

    update.message.reply_text(message, reply_markup=reply_markup)

import csv

def button(update, context):
    data2 = pd.read_csv('result.csv', encoding='utf8')
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    username = update.effective_user.username
    user.clear()
    for x in data2['username']:
        user.append(x) 
    print(user.count(username))   
    if(int(user.count(username)) == 25):
        query.edit_message_text(text="አንኳን ደስ አሎት የ5 ብር ካርድ አሸናፊ ሆነዋል!")
        write(query,username)
        return 0
    if(int(user.count(username)) == 50):
        query.edit_message_text(text="አንኳን ደስ አሎት የ10 ብር ካርድ አሸናፊ ሆነዋል!")
        write(query,username)
        return 0
    if(int(user.count(username)) == 100):
        query.edit_message_text(text="አንኳን ደስ አሎት የ15 ብር ካርድ አሸናፊ ሆነዋል!")
        write(query,username)
        return 0
    if(int(user.count(username)) == 200):
        query.edit_message_text(text="አንኳን ደስ አሎት የ25 ብር ካርድ አሸናፊ ሆነዋል!")
        write(query,username)
        return 0
    if(int(user.count(username)) == 400):
        query.edit_message_text(text="አንኳን ደስ አሎት የ50 ብር ካርድ አሸናፊ ሆነዋል!")
        write(query,username)
        return 0
    if(int(user.count(username)) == 1000):
        query.edit_message_text(text="አንኳን ደስ አሎት የ100 ብር ካርድ አሸናፊ ሆነዋል!")
        write(query,username)
        return 0
    if(int(user.count(username)) == 3000):
        query.edit_message_text(text="አንኳን ደስ አሎት የ200 ብር ካርድ አሸናፊ ሆነዋል!")
        write(query,username)
        return 0
    if(int(user.count(username)) == 6000):
        query.edit_message_text(text="አንኳን ደስ አሎት የ400 ብር ካርድ አሸናፊ ሆነዋል!")
        write(query,username)
        return 0
    
       
    write(query,username)
    tweet_id, tweet = random.choice(list(map.items()))
    
    if tweet_id not in map2:
        text[tweet_id] = tweet
    
    message = tweet
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=message)
    query.edit_message_reply_markup(reply_markup=reply_markup)

   

def write(query,username):
    for key in text:
        text[key] = format(query.data)
    
    with open('result.csv', 'a') as f:
        writer = csv.writer(f)
        for key, value in text.items(): 
            writer.writerow([key,value,str(username)])
    text.clear()


def help(update, context):
    update.message.reply_text("Use /start to test this bot.")

def end(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text='ስለ ትብብሮ እናመሰግናለን!')

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    updater.dispatcher.add_handler(CommandHandler('end', end))
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()
'''
@server.route("/" + TOKEN, methods = ['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode('utf-8'))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://dataannotatort.com/" + TOKEN)
    return "!", 200
'''     

if __name__ == '__main__':
    main()


