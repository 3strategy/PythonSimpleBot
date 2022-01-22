# for the different states and algorithm to implement see README.md
import os
import telebot
from user import User, State

st1='\nבתשאול זה מופעלות ההנחיות מה-30/12'

API_KEY = os.getenv('API7_KEY')
bot = telebot.TeleBot(API_KEY)
users = []
def get_user(chat_id):
  for u in users:
    if u.chat_id == chat_id:
      return u
  new_user = User(chat_id)
  users.append(new_user)
  return new_user
@bot.message_handler(commands=['Greet'])  #this type of command will require user to type /Greet
def greet(message):
  bot.reply_to(message, "Hey! Hows it going?")  # this does a reply

@bot.message_handler(commands=['help']) #this vent triggers when user types /help
def help(message):
  # we will use this as start over.
  user = get_user(message.chat.id)
  user.state = State.UNKNOWN
  bot.send_message(message.chat.id, "מה קורה. הפקודות האפשרויות הן ככה וככה")  # כאן מקובל להציג את מערכת הפקודות הנתמכת במערכת

@bot.message_handler(regexp='נחשפתי')  # this will be accepted without "/" and at any capitalization
def hello(message):
  user = get_user(message.chat.id)
  bot.send_message(message.chat.id, f'סבבה, אבל כרגע לא נתמך 19\n{user.state}\n/help')  # this merely sends a message


@bot.message_handler(regexp='State')  # for debug purposes
def hello(msg):
  user = get_user(msg.chat.id)
  bot.send_message(msg.chat.id, user.state)  # this merely sends a message

@bot.message_handler(regexp='כן')
def hello(msg):
  user = get_user(msg.chat.id)
  if user.state == State.NAMED: #we just expecting his exposed or not answer
    user.state = State.S1_EXPOSED
    bot.send_message(msg.chat.id, "האם הנך מחוסן (תו ירוק בתוקף)?")  # this merely sends a message
  elif user.state == State.S1_EXPOSED: #we are expecting his immuned or not answer
    user.state = State.S3_IMMUNE
    bot.send_message(msg.chat.id, "נפלא\nגש מיד לבדיקת אנטיגן מוסדית\nהאם האנטיגן המוסדי חיובי?")  # this merely sends a message

  else:
    bot.send_message(msg.chat.id, f'עדיין לא מקודד. 18\n{user.state}')

@bot.message_handler(regexp='לא')
def hello(msg):
  user = get_user(msg.chat.id)
  if user.state == State.NAMED: #the NO response here is an answer to "exposed or not"
    user.state == State.S0_NOT_EXPOSED
    bot.send_message(msg.chat.id, "המשך יום נעים")  # this merely sends a message
  elif user.state == State.S1_EXPOSED: #we are expecting his immuned or not answer
    user.state = State.S2_NOT_IMMUNE
    bot.send_message(msg.chat.id, "אוי ואבוי,\nגש מיד לבדיקת PCR\nהאם ה-PCR חיובי?")  # this merely sends a message
  else:
    bot.send_message(msg.chat.id, f'עדיין לא מקודד. 20\n{user.state}')

@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(msg):
    # this is the standard reply to a normal message
    # it has to be used when user sends his name.
    # this type of default handler can mask other handlers. It must be located at the end.
    user = get_user(msg.chat.id)
    if user.state == State.UNKNOWN: #it's a brand new user
      user.state = State.ANONYMOUS
      bot.send_message(msg.chat.id, "לא הבנתי. כתוב את שמך או\n להתחלה מחדש שלח  \n/help")
    elif user.state == State.ANONYMOUS: #already known:
      user.name = msg.text # take message as a name
      print(user.name, user.chat_id)
      user.state = State.NAMED
      bot.send_message(msg.chat.id, f'הי {user.name},\n האם נחשפת?\nמשלב זה עליך לענות רק כן או לא!{st1}')
    else:
      #not sure why we are here. (Unhanled situation was reached)
      bot.send_message(msg.chat.id, f'הי, המצב כרגע לא ברור 17.\n נסה שוב מאוחר יותר\n {user.state}\nלהתחלה מחדש שלח\n/help')

bot.polling()  # keeps the bot running and accepting messages