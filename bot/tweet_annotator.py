from telegram.error import ChatMigrated, BadRequest, Unauthorized, TimedOut, NetworkError
from telegram.ext import Updater
from telegram import Poll, Bot, PollOption, User, TelegramError
import os
# import telepot
import random
import csv
import pandas as pd
from flask import Flask, request
from properties.p import Property
from datetime import datetime
from threading import Lock, Thread
from datetime import date
import time

# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.message import EmailMessage

from telegram.utils.request import Request

lock = Lock()


user_real = {}
prop = Property()

max_allowed_tweet = 500  # 500 tweets
bot_prop = prop.load_property_files('bot.properties')

annotated_tweet_ids = []
tweet_id_time = {}
users = []
if not os.path.exists('annotated_tweets.csv'):
    columns = ['tweet_id', 'sentiment', 'tweet', 'username']
    df = pd.DataFrame(columns=columns)
    df.to_csv('annotated_tweets.csv', index=False)
else:
    data2 = pd.read_csv('annotated_tweets.csv', encoding='utf8')
    annotated_tweet_ids = data2['tweet_id'].apply(lambda x: str(x)).tolist()
    sentiment = data2['sentiment']
    count = data2['username'].value_counts()
    users = data2['username'].tolist()

ans = list()
if not os.path.exists('control_questions.csv'):
    columns = ['tweet', 'class']
    df = pd.DataFrame(columns=columns)
    df.to_csv('control_questions.csv', index=False)
else:
    control_questions = pd.read_csv('control_questions.csv', encoding='utf8')
    for item in zip(control_questions['tweet'], control_questions['class']):
        ans.append((item[0], item[1]))

control = []
if not os.path.exists('control_answers.csv'):
    columns = ['tweet', 'answer', 'username']
    df = pd.DataFrame(columns=columns)
    df.to_csv('control_answers.csv', index=False)
else:
    control_answers = pd.read_csv('control_answers.csv', encoding='utf8')
    for item in zip(control_answers['tweet'], control_answers['answer'], control_answers['username']):
        control.append((item[0], item[1], item[2]))

if not os.path.exists('rewarded_cards.txt'):
    f = open('rewarded_cards.txt', 'w', encoding='utf8')
    f.close()

blocked_users = []
if not os.path.exists('blocked_user.txt'):
    f = open('blocked_user.txt', 'w', encoding='utf8')
    f.close()
else:
    blocked_users = open('blocked_user.txt', 'r').read()

data = pd.read_csv('raw_tweets.csv', encoding='utf8', header=0)
raw_tweet_ids = data['tweet_id']

tweet = data['tweet']
user = []

user_tweet_ids = {}  # username1 = tweet_id1, username2 = annotated_tweet_ids

map = dict()
map2 = dict()
for item in raw_tweet_ids.keys():
    map[raw_tweet_ids[item]] = tweet[item]

# converting to dict

# display


# bot = telebot.TeleBot(token = TOKEN)
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

    username = update.effective_user.username
    if username in blocked_users:
        update.message.reply_text(text="እባክዎን በሚቀጥላው ኢሜይል ያግኙን: hizkiel.mitiku@studio.unibo.it")
        return 0

    if len(get_five_birs()) + len(get_ten_birs()) == len(get_charged_cards()) or \
            (len(get_five_birs()) % 2 == 1 and
             len(get_five_birs()) + len(get_ten_birs()) - 1 == len(get_charged_cards())):
        update.message.reply_text(text="ትንሽ ቆይተው ይሞክሩ!")
        send_email()
        return 0

    del_timeout_users()

    if username in user_tweet_ids and user_tweet_ids[username]:
        update.message.reply_text(text="እባክዎን ከላይ ያለውን መጀመሪያ ይሙሉ!")
        return 0
    # else:

    if username == None:
        update.message.reply_text(
            text="እባክዎን በመጀመሪያ ዩዘርኔም ሴቲንግ ውስጥ ገብተው ይፍጠሩ:: Settings-->click 'username'--> add username here.  ስለ ዩዘርንም አፈጣጠር ለማወቅ ይህንን ቪድዮ ይመልከቱ https://www.youtube.com/watch?v=AOYu40HTQcI&feature=youtu.be")
        return 0
    # f   = open('ids.txt', 'r', encoding='utf8')
    # ids = f.read().strip().split("\n")

    user.clear()
    reply_markup = InlineKeyboardMarkup(keyboard)

    lock.acquire()
    if (len(annotated_tweet_ids) == len(raw_tweet_ids)):
        message = 'ሁሉም ዳታ ተሞልቷል በቀጣይ ተጨማሪ ሲኖር እናሳውቀዎታለን፤ እናመሰግናለን!!'
        update.message.reply_text(message)
        return 0
    else:
        for x in raw_tweet_ids:
            if x not in annotated_tweet_ids:
                if username in user_tweet_ids and user_tweet_ids[username] != None:
                    break
                else:
                    if x not in [user_tweet_id for user_tweet_id in user_tweet_ids.values()]:
                        user_tweet_ids[username] = x
                        annotated_tweet_ids.append(x)
                        tweet_id_time[username] = time.time()
                        break
    update.message.reply_text(map[user_tweet_ids[username]], reply_markup=reply_markup)
    lock.release()


def del_timeout_users():
    expired_users = []
    for uname in tweet_id_time:
        current_time = time.time()
        if current_time - tweet_id_time[uname] > 600:
            expired_users.append(uname)
            annotated_tweet_ids.remove(user_tweet_ids[uname])
            user_tweet_ids[uname] = None

    for expired_user in expired_users:
        del tweet_id_time[expired_user]


def send_email():
    import smtplib, ssl

    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = "tellebott@gmail.com"
    receiver_email = "hizclick@gmail.com"
    password = "Hizbot2020"
    message = """no more mobile cards"""

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)


def get_control_question():
    control_question = pd.read_csv("control_questions.csv", encoding='utf8', usecols=['tweet', 'class'])
    return control_question


def verify(username):
    counter = 0
    message = None
    user_tweet = []
    for item in control:
        if username == item[2]:
            user_tweet.append((item[0], item[1]))

    if len(user_tweet) > 2:  # more than two mistakes
        for x in range(max(len(user_tweet) - 4, 0), len(user_tweet)):
            if user_tweet[x] in ans:
                break
            else:
                counter = counter + 1
            if counter == 3:
                message = "warning"
            elif counter > 3:
                message = "block"

    if counter >= 4:
        with open('blocked_user.txt', 'a', encoding='utf8') as f:
            blocked_users.append(username)
            f.write(username)
    return message

def get_charged_cards():
    fil = open('rewarded_cards.txt', 'r', encoding='utf8')
    rewarded_cards = fil.readlines()
    re = []
    for x in rewarded_cards:
        j = x.replace(' ', '')
        re.append(j.rstrip('\n').split('\t')[0])
    while ('' in re):
        re.remove('')
    return re

def get_ten_birs():
    f2 = open('10birr.txt', 'r', encoding='utf8')
    ten = f2.readlines()
    te = []
    for x in ten:
        j = x.strip()
        te.append(j.rstrip('\n'))
    while ('' in te):
        te.remove('')

    return te


def get_five_birs():
    f = open('5birr.txt', 'r', encoding='utf8')
    five = f.readlines()
    fiv = []
    for x in five:
        j = x.strip()
        fiv.append(j.rstrip('\n'))
    while ('' in fiv):
        fiv.remove('')

    return fiv


def prise(num, username):

    lock.acquire()
    message = "እንኳ ደስ አለዎት የ" + str(num) + " ብር ካርድ አሸናፊ ሆነዋል። የካርድ ቁጥርዎ የሚከተሉት ናቸው፦ "
    fiv = get_five_birs()
    re = get_charged_cards()
    te = get_ten_birs()

    user_cards = []
    user_cards.extend(re)
    number = ''
    '''
    if len(te) > len(re):
        for n in te:
            if str(n) not in re:
                user_cards.append(n)
                number = number + ' ካርድ ቁጥር :- ' + str(n)
                fil = open('rewarded_cards.txt', 'a', encoding='utf8')
                fil.writelines(str(n) + '\t' + '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.now()) + '\n')
                fil.close()
                break
    

    else:
    '''
    cnt = 0
    if len(te) > len(re):
        for n in te:
            if str(n) not in user_cards:
                user_cards.append(n)
                number = number + ' ካርድ ቁጥር :- ' + str(n)
                fil = open('rewarded_cards.txt', 'a', encoding='utf8')
                fil.writelines(str(n) + '\t' + '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.now()) + "\n")
                fil.close()
                break
    else:
        for n in fiv:
            if str(n) not in user_cards:
                user_cards.append(n)
                number = number + ' ካርድ ቁጥር :- ' + str(n)
                fil = open('rewarded_cards.txt', 'a', encoding='utf8')
                fil.writelines(str(n) + '\t' + '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.now()) + "\n")
                fil.close()
                cnt += 1
                if cnt > 1:
                    break
    lock.release()
    return message + number



def button(update, context):
    del_timeout_users()

    query = update.callback_query
    if len(get_five_birs()) + len(get_ten_birs()) <= len(get_charged_cards()):
        query.edit_message_text(text="ትንሽ ቆይተው ይሞክሩ!")
        print("+++++++++ADMINS, Please add cards to continue the annotation.+++++")
        send_email()
        return 0

    message_id = update.callback_query.message.message_id
    print(message_id)
    username = update.effective_user.username
    if username == None:
        query.edit_message_text(
            text="እባክዎን በመጀመሪያ ዩዘርኔም ሴቲንግ ውስጥ ገብተው ይፍጠሩ::Settings-->Edit Profile-->Add username--Save. ለበለጠ መረጃ https://www.youtube.com/watch?v=AOYu40HTQcI&feature=youtu.be")
        return 0
    user.clear()

    # f   = open('ids.txt', 'r', encoding='utf8')
    # ids = f.read().strip().split("\n")

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    user.clear()
    for x in users:
        user.append(x)
    coun = user.count(username)  # TODO
    val = coun % 6

    if (int(coun) > max_allowed_tweet):
        query.edit_message_text(text="ሁሉም ዳታ ተሞልቷል እስካሁን የሞሉት ዳታ ተመዝግቦ ተቀምጧል፣ በቀጣይ ዳታ ብቅርብ ጊዜ እንለቃለን፣ ተመልሰው ይሞክሩ!!")
        return 0

    # if (coun % 50 == 0 and coun != 0):
    if coun % 5 == 0 and coun != 0:
        pr = prise(10, username) + " ለመቀጠል /start ይጫኑ!"
        write(query, username)
        query.edit_message_text(text=pr)
        return 0

    if user_tweet_ids[username]:
        write(query, username)

    if (len(annotated_tweet_ids) == len(raw_tweet_ids)):
        message = 'ሁሉም ዳታ ተሞልቷል እስካሁን የሞሉት ዳታ ተመዝግቦ ተቀምጧል፣ በቀጣይ ዳታ በቅርብ ጊዜ እንለቃለን፣ ተመልሰው ይሞክሩ!!'
        query.edit_message_text(text=message)
        return 0
    else:
        for x in raw_tweet_ids:
            if x not in annotated_tweet_ids:
                if user_tweet_ids[username]:
                    break
                elif x not in [user_tweet_id for user_tweet_id in user_tweet_ids.values()]:
                    user_tweet_ids[username] = x
                    annotated_tweet_ids.append(x)
                    tweet_id_time[username] = time.time()
                    eval(query, x, map[user_tweet_ids[username]], username)
                    break
    if val == 0:

        reply_markup = InlineKeyboardMarkup(keyboard)
        user_real[username]  = real_control()
        query.edit_message_text(text=user_real[username])
        query.edit_message_reply_markup(reply_markup=reply_markup)
        write_correct(query,username,user_real[username])
        message = verify(username)
        if message == 'warning':
            query.edit_message_text(text="ተደጋጋሚ ስህተት እየሰሩ ነው፤ እባክዎን ተጠንቅቀው ይሙሉ, ለመቀጠል /start ይጫኑ!")
            user_tweet_ids[username] = None
            return 0
        elif message == 'block':
            query.edit_message_text(text="ተደጋጋሚ ስህተት ስለ ሰሩ አካውንቶ ታግዶአል፡፡")
            return 0




def write_correct(query, username, message):
    with open('control_answers.csv', 'a', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow([message, format(query.data), str(username)])
        control.append((message, format(query.data), str(username)))
        user_real[username] = None


def eval(query, tweet_id, tweet, username):
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=tweet)
    query.edit_message_reply_markup(reply_markup=reply_markup)


def real_control():
    import random
    tweet = list()
    for item in ans:
        tweet.append(item[0])
    return random.choice(tweet)


def write(query, username):
    with open('annotated_tweets.csv', 'a', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow([user_tweet_ids[username], format(query.data), map[user_tweet_ids[username]], str(username)])
        print([user_tweet_ids[username], format(query.data), map[user_tweet_ids[username]], str(username)])
        user_tweet_ids[username] = None
        users.append(username)


def help(update, context):
    update.message.reply_text("Use /start to test this bot.")


def end(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='ስለ ትብብርዎ እናመሰግናለን!')


def error(update, context):
    try:
        raise error
    except Unauthorized:
        logging.debug("TELEGRAM ERROR: Unauthorized - %s" % error)
    except BadRequest:
        logging.debug("TELEGRAM ERROR: Bad Request - %s" % error)
    except TimedOut:
        logging.debug("TELEGRAM ERROR: Slow connection problem - %s" % error)
        message = 'Timeout, /start የሚለውንንይሞክሩ!'
        query = update.callback_query
        update.message.reply_text(text=message)
    except NetworkError:
        logging.debug("TELEGRAM ERROR: Other connection problems - %s" % error)
    except ChatMigrated as e:
        logging.debug("TELEGRAM ERROR: Chat ID migrated?! - %s" % error)
    except TelegramError:
        logging.debug("TELEGRAM ERROR: Other error - %s" % error)
    except:
        logging.debug("TELEGRAM ERROR: Unknown - %s" % error)
        """Log Errors caused by Updates."""
        logger.warning('Update "%s" caused error "%s"', update, context.error)
        message = 'እባክዎ እንደገና ይሞክሩ, /start የሚለውንንይሞክሩ!'
        query = update.callback_query
        query.edit_message_text(text=message)
    return 0


def instruction(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='ጽሁፉ ገምቢ ከሆነ "ገምቢ" የሚለውን፣ አፍራሽ ከሆነ "አፍራሽ" የሚለውን፣ ገለልትኛ "ገለልተኛ" የሚለውን ፣ የገምቢ እና የአፍራሽ ቅልቅል ከሆነ "ቅልቅል" የሚለውን ይምረጡ፡፡ ይህንን መረጃ ሲሞሉ በትክክል በመለሱት ጥያቄ ልክ በዕለቱ መጨረሻ በእርስዎ "user name" በኩል የሞባይል ካርድ ሽልማት ይላክለዎታል። ለበለጠ መረጃ https://annotation-wq.github.io/')


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


if __name__ == '__main__':
    main()

