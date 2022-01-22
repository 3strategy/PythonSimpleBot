
import os
import telebot

API_KEY = os.getenv('API7_KEY')
bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['Greet'])  #this type of command will require user to type /Greet
def greet(message):
  bot.reply_to(message, "Hey! Hows it going?")  # this does a reply

@bot.message_handler(regexp='hello')  # this will be accepted without / and at any capitalization
def hello(message):
  bot.send_message(message.chat.id, "Hello!")  # this merely sends a message

bot.polling()  # keeps the bot running and accepting messages