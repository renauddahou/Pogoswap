from telegram.ext import Updater, CommandHandler, RegexHandler, MessageHandler,Filters,CallbackQueryHandler
from telegram import ReplyKeyboardMarkup,ReplyKeyboardRemove,InlineKeyboardMarkup,InlineKeyboardButton,ParseMode,Bot
import requests,json
import os
import streamlit as st
from datetime import datetime
import time
now = datetime.now()
current_time = now.strftime("%H:%M:%S")

#Bot HSE
user_input3 = "salut"
response3 = user_input3
st.text_area("HSEBot:", value=response3, height=200, max_chars=None, key=None)

config = json.load(open('config.json','r'))

TOKEN = config['token']
DEV = True
signup = config['signup']
admins = config['admins']
refr = config['ref']
tkn = config['token_name']
tgk = config['telegram_kanal']
tgc = config['telegram_chat']
tw = config['twitter']
twp = config['twitter_post']
website = config['website']
data = []
dash_key = [['💰Balance','👥Referral'],['👨‍💻Profile','📈About'],['💣Withdraw','🧰Support']]
continue_key = [['Continue👌']]
completed_key = [['Completed✅']]
admin_key = [["Total_users", "Database", "Newsletter"]]

#webhook_url = 'Your Webook' #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#PORT = int(os.environ.get('PORT','8443'))


def start(update, context): #command
    if update.message.chat.type == 'private':
        user = str(update.message.chat.username)
        if user not in data['users']:
            data['users'].append(user)
            if user not in data['chat_id']: #######
                chat1id = str(update.message.chat.id)
                data['chat_id'].append(chat1id)
            if user not in data['twitter']:
                data['twitter'][user] = ""
            if user not in data['Youtube']:
                data['Youtube'][user] = ""
            if user not in data['bep20']:
                data['bep20'][user] = ""
            if user not in data['mail']:
                data['mail'][user] = ""
            ref_id = update.message.text.split()
            if len(ref_id) > 1:
                data['ref'][user] = ref_id[1]
                if str(ref_id[1]) not in data['referred']:
                    data['referred'][str(ref_id[1])] = 1
                else:
                    data['referred'][str(ref_id[1])] += 1
            else:
                data['ref'][user] = 0
            data['total'] += 1
            data['id'][user] = data['total']
            msg = config['intro'] + '\n[WEBSITE]({})'.format(website) #INTRO
            #ПРИМЕР "*bold* _italic_ `fixed width font` [link](http://google.com)\.",parse_mode= 'MarkdownV2'
            reply_markup = ReplyKeyboardMarkup(continue_key,resize_keyboard=True) #кнопка продолжить
            #update.message.reply_text(msg, parse_mode= 'MarkdownV2',disable_web_page_preview=True,reply_markup=reply_markup) #----+вывод интр
            update.message.reply_text(msg,reply_markup=reply_markup) #----+intro output
            data['process'][user] = "Continue"
            json.dump(data,open('users.json','w'))
            
        else:
            welcome_msg = "Welcome Back"
            reply_markup = ReplyKeyboardMarkup(dash_key,resize_keyboard=True) #dash_key
            update.message.reply_text(welcome_msg,reply_markup=reply_markup) #----

    else:
        msg = '{} \n. I don\'t reply in group, come in private'.format(config['intro'])
        update.message.reply_text(msg)
        
        


def profile(update, context):
    if update.message.chat.type == 'private':
        user = str(update.message.chat.username)
        mail = data['mail'][user]
        twi = data['twitter'][user]
        ytb = data['Youtube'][user]
        bep20_addr = data['bep20'][user]
        msg = 'Your Provided Data:\n\n    Name: {}\n\n    E-mail: {}\n\n    Twitter: {}\n\n    Youtube: {}\n\n    bep20 Address: {}'.format(user,mail,twi,ytb,bep20_addr)
        reply_markup = ReplyKeyboardMarkup(dash_key,resize_keyboard=True)
        update.message.reply_text(msg,reply_markup=reply_markup)

def about(update, context): #command
    if update.message.chat.type == 'private':
        msg = config['about'] + '\n[WEBSITE]({})'.format(website)
        reply_markup = ReplyKeyboardMarkup(dash_key,resize_keyboard=True)
        #update.message.reply_text(msg,parse_mode= 'MarkdownV2',disable_web_page_preview=True,reply_markup=reply_markup)
        update.message.reply_text(msg,reply_markup=reply_markup)

def withdraw(update, context): #command
    if update.message.chat.type == 'private':
        msg = "💣You will be able to withdraw on {}".format(config['withdraw_data'])
        reply_markup = ReplyKeyboardMarkup(dash_key,resize_keyboard=True)
        update.message.reply_text(msg,reply_markup=reply_markup)

def support(update, context): #command
    if update.message.chat.type == 'private':
        msg ="🧰 Contact support:@Bluecolo"
        reply_markup = ReplyKeyboardMarkup(dash_key,resize_keyboard=True)
        #update.message.reply_text(msg,parse_mode= 'MarkdownV2',disable_web_page_preview=True,reply_markup=reply_markup)
        update.message.reply_text(msg,reply_markup=reply_markup)

def extra(update, context): #command
    if update.message.chat.type == 'private':
        user = str(update.message.chat.username)
        if data["process"][user] == 'Continue':
            msg = "👋Hey {}".format(user) + "\n\n➡️Lets get you started:\n🔷Join [Telegram Group]({})".format(tgc) + "\n🔷Join [Youtube Channel]({}) and made a positive comment on one of our posts".format(tgk) + "\n🔷Follow us on [Twitter]({}) and made a positive comment on one of our posts".format(tw) + "\n\n⚠️Note: _We'll check your all information manually\._\n" + "_So complete all tasks properly then click_ *\"Completed✅\"*\n\n_If you click on completed without having executed the tasks you will not be able to withdraw token even if the bot grants it to you because our team checks thoroughly before validating the transfer to your bep20 address\._\n"
            reply_markup = ReplyKeyboardMarkup(completed_key,resize_keyboard=True)
            update.message.reply_text(msg,parse_mode= 'MarkdownV2',disable_web_page_preview=True,reply_markup=reply_markup)
            data['process'][user] = "Completed"
            json.dump(data,open('users.json','w'))
            
        elif data["process"][user] == 'Completed':
            started_msg = "\n🔷Follow us on [Twitter]({})".format(tw) + " and retweet this [post]({})".format(twp) +"\n\n⚠️Then submit your Twitter username with @:"
            data['process'][user] = "twitter"
            json.dump(data,open('users.json','w'))
            
            reply_markup = ReplyKeyboardRemove(bool = False)
            update.message.reply_text(started_msg,parse_mode= 'MarkdownV2',disable_web_page_preview=True,reply_markup=reply_markup)
        elif data["process"][user] == 'twitter':
            msg = "⚠️Then submit your Youtube username with @:"
            data['Youtube'][user] = update.message.text
            data['process'][user] = 'Youtube'
            json.dump(data,open('users.json','w'))
            
            update.message.reply_text(msg)    
        elif data["process"][user] == 'Youtube':
            msg = "📧Please type below your E-mail:"
            data['twitter'][user] = update.message.text
            data['process'][user] = 'mail'
            json.dump(data,open('users.json','w'))
            
            update.message.reply_text(msg)
        elif data["process"][user] == 'mail':
            data['mail'][user] = update.message.text
            data['process'][user] = "bep20"
            json.dump(data,open('users.json','w'))
            
            update.message.reply_text("👍Almost done,Now submit your BEP-20 address below:\n\n⚠️ Note: Don't send me any exchanger wallet address:")
        elif data["process"][user] == 'bep20':
            data['bep20'][user] = update.message.text
            data['process'][user] = "finished"
            json.dump(data,open('users.json','w'))
            
            msg = "🎉Congratulations!\nYou have successfully completed all airdrop tasks."
            reply_markup = ReplyKeyboardMarkup(dash_key,resize_keyboard=True)
            update.message.reply_text(msg,reply_markup=reply_markup)
        elif data["process"][user] == 'post':
            inp = update.message.text
            bot = Bot(TOKEN)
            ny = 0
            nn = 0
            for u in data['chat_id']:
                try:
                    bot.send_message(u, inp, parse_mode= 'MarkdownV2',disable_web_page_preview=True)# parse_mode = 'MarkdownV2',disable_web_page_preview=True
                    ny = ny + 1
                except:
                    nn = nn + 1
                    pass
            msg = '✅ {}\n❌ {}'.format(ny, nn)
            update.message.reply_text(msg)
            data['process'][user] = "finished"
        else:
            msg = "Please select one of the options."
            reply_markup = ReplyKeyboardMarkup(dash_key,resize_keyboard=True)
            update.message.reply_text(msg,reply_markup=reply_markup)

def ref(update, context): #command
    if update.message.chat.type == 'private':
        user = str(update.message.chat.username)
        i = str(data["id"][user])
        referred = 0
        if i in data['referred']:
            referred = data['referred'][i]
        msg = "⛏To increase your balance refer more friends using your referral link, you will earn {} {} for each person you refer.\n\n🎁Referral link: https://t.me/{}?start={} \n \n👥You have {} Referrals".format(config['ref'],tkn,config['botname'],data['id'][user],referred)
        reply_markup = ReplyKeyboardMarkup(dash_key,resize_keyboard=True)
        update.message.reply_text(msg,reply_markup=reply_markup)

def admin(update, context): #command
    if update.message.chat.type == 'private':
        user = str(update.message.chat.username)
        if user in admins:
            msg = "Welcome to Admin Dashboard"
            reply_markup = ReplyKeyboardMarkup(admin_key,resize_keyboard=True)
            update.message.reply_text(msg,reply_markup=reply_markup)

def users(update, context): #command
    if update.message.chat.type == 'private':
        user = str(update.message.chat.username)
        if user in admins:
            msg = "A total of {} have joined this program".format(data['total']-10000)
            reply_markup = ReplyKeyboardMarkup(admin_key,resize_keyboard=True)
            update.message.reply_text(msg,reply_markup=reply_markup)

def get_file(update, context): #command
    if update.message.chat.type == 'private':
        user = str(update.message.chat.username)
        if user in admins:
            fileToArchive = time.strftime("Date_%Y_%m_%d_@_Time_%Hh_%Mm_%Ss")
            f = open(fileToArchive+'users.csv','w')
            f.write("id,username,twitter username,Youtube username,bep20 address,mail,no. of persons referred,referred by\n")
            for u in data['users']:
                i = str(data['id'][u])
                refrrd = 0
                if i in data['referred']:
                    refrrd = data['referred'][i]
                d = "{},{},{},{},{},{},{}\n".format(i,u,data['twitter'][u],data['Youtube'][u],data['bep20'][u],data['mail'][u],refrrd,data['ref'][u])
                f.write(d)
                
            f.close()
            
            bot = Bot(TOKEN)
            bot.send_document(chat_id=update.message.chat.id, document=open(fileToArchive+'users.csv','rb'))
            bot = Bot(TOKEN)
            bot.send_document(chat_id=update.message.chat.id, document=open('users.json','rb'))
            
            
            
            
#
def bal(update, context): #command
    if update.message.chat.type == 'private':
        user = str(update.message.chat.username)
        i = str(data["id"][user])
        referred = 0
        if i in data['referred']:
            referred = data['referred'][i]
        bal = signup + refr * referred
        refbal = refr * referred
        msg = "💵Balance: {} + {} {}\n\n👥Refferal Count: {}\n\n💰Total Balance: {}\n\n Click Referral Button to Accumulate more {}".format(signup, refbal, tkn, referred, bal, tkn, tkn)
        reply_markup = ReplyKeyboardMarkup(dash_key,resize_keyboard=True)
        update.message.reply_text(msg,reply_markup=reply_markup)

def mailing(update, context):
    if update.message.chat.type == 'private':
        user = str(update.message.chat.username)
        if user in admins:
            update.message.reply_text('Enter the post:')
            data["process"][user] = "post"



if __name__ == '__main__':
    data = json.load(open('users.json','r'))
    updater = Updater(TOKEN,use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start",start)) #command handlers
    dp.add_handler(CommandHandler("admin",admin))
    dp.add_handler(RegexHandler("^👨‍💻Profile$",profile))
    dp.add_handler(RegexHandler("^📈About$",about))
    dp.add_handler(RegexHandler("^💣Withdraw$",withdraw))
    dp.add_handler(RegexHandler("^🧰Support$",support))
    dp.add_handler(RegexHandler("^👥Referral$",ref))
    dp.add_handler(RegexHandler("^💰Balance$",bal))
    dp.add_handler(RegexHandler("^Total_users$",users))
    dp.add_handler(RegexHandler("^Newsletter$",mailing))
    dp.add_handler(RegexHandler("^Database$",get_file))
    dp.add_handler(MessageHandler(Filters.text,extra))
    updater.start_polling()
    print("Bot Started")
    updater.idle()
        


#telegram.error.RetryAfter: Flood control exceeded. Retry in 3 seconds increase timeout time
