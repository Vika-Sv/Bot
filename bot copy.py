import telebot
import openai
import a
from config import BOT_TOKEN, API_KEY


bot = telebot.TeleBot(BOT_TOKEN) 

@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id,'Привіт, рада тебе бачити сьогодні!)')
    

@bot.message_handler()

def info (message):
    if message.text.lower() == 'привіт':
        bot.reply_to(message, f'Привіт, {message.from_user.first_name}')  

    
bot.polling(none_stop= True)