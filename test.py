from telegram.ext import Updater
from telegram import Poll, Bot, PollOption
import os
from flask import Flask, request

import telebot

TOKEN = '<api_token>'
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

TOKEN = '1022567655:AAGjqp1EcNQKQlFlzMIr6MpLQLIoi_YJ4YM'

updater = Updater(token=TOKEN, use_context=True)

server = Flask(__name__)

text = open('test.txt', "r", encoding="utf-8")

lines = text.readlines()


@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://sentimentannotator.com/' + TOKEN)
    return "!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

dispatcher = updater.dispatcher

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def start(update, context):
    global lines
    context.bot.send_message(chat_id=update.effective_chat.id, text=lines[0])


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
            context.bot.send_message(chat_id=update.effective_chat.id, text=lines[count])
            with open('test.txt', 'w', encoding="utf-8") as fout:
                fout.writelines(lines[1:])
            text = open('test.txt', "r", encoding="utf-8")
            lines = text.readlines()
            with open('test2.txt', 'a', encoding="utf-8") as f: 
                f.writelines(update.message.text+"\n")
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
