# for the different states and algorithm to implement see README.md
import os
import telebot
from user import User, St

debug = True
st1='\nבתשאול זה מופעלות ההנחיות מה-19/01'
q60='האם אתה בן 60 ומעלה או נמצא בסיכון?'
q_res = '\nהאם קיבלת תוצאה חיובית?'
pIso = f'עליך לבצע PCR 72 שעות ממועד החשיפה. או מרגע הופעת סימפטומים. חייב בבידוד עד לקבלת תוצאות הבדיקה.{q_res}'
pNoIso = f'עליך לבצע PCR 72 שעות ממועד החשיפה. או מרגע הופעת סימפטומים. אינך חייב בבידוד בשלב זה.{q_res}'
aNoIso = f'אינך חייב בבידוד. עליך לבצע אנטיגן ביתית או מוסדית 72 שעות ממועד החשיפה.{q_res}'
aIso = f'הינך חייב בבידוד של 5 ימים. מומלץ לבצע בדיקת אנטיגן בייתית 72 שעות ממועד החשיפה. הנך חייב בבדיקת אנטיגן מוסדית לאחר 5 ימים.{q_res}'

release = f'\nשחרור מבידוד לאחר 2 בדיקות אנטיגן ביתיות שליליות ביום הרביעי והחמישי לבידוד ובתנאי שאין תסמינים.{q_res}'
iso5_2Net = f'חייב בבידוד 5 ימים.{release}'
free = f'שחרור מבידוד'
exempt = f'פטור מבידוד'
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
def help(message):   # we will use this as start over.
  u = get_user(message.chat.id)
  u.state = St.ANONYMOUS  # instead of defaulting to UNKNOWN
  bot.send_message(message.chat.id, "הי, מה שמך?\nלהתחלה מחדש שלח  \n/help")  # כאן מקובל להציג את מערכת הפקודות הנתמכת במערכת

@bot.message_handler(regexp='נחשפתי')  # this will be accepted without "/" and at any capitalization
def hello(message):
  u = get_user(message.chat.id)
  bot.send_message(message.chat.id, f'סבבה, אבל כרגע לא נתמך 19\n{u.state}\n/help')  # this merely sends a message


@bot.message_handler(regexp='State')  # for debug purposes
def hello(msg):
  u = get_user(msg.chat.id)
  bot.send_message(msg.chat.id, u.state)  # this merely sends a message

@bot.message_handler(regexp='כן')
def hello(msg):
  u = get_user(msg.chat.id)
  if u.state == St.NAMED: #we just expecting his exposed or not answer
    u.state = St.S1_EXPOSED
    bot.send_message(msg.chat.id, "האם הנך מחוסן (תו ירוק בתוקף)?")  # this merely sends a message

  elif u.state == St.S1_EXPOSED: #we are expecting his immuned or not answer
    u.state = St.S3_IMMUNE
    bot.send_message(msg.chat.id, q60) # age question


  elif u.state == St.S3_IMMUNE:
    u.state = St.S17_SIXTY
    bot.send_message(msg.chat.id, pNoIso)


  elif u.state == St.S17_SIXTY:
    u.state = St.S23_
    bot.send_message(msg.chat.id, iso5_2Net)
    if debug: bot.send_message(msg.chat.id,f'67:{u.state}')

  elif u.state == St.S2_NOT_IMMUNE:
    u.state = St.S15_SIXTY
    bot.send_message(msg.chat.id, pIso)
    if debug: bot.send_message(msg.chat.id,f'72:{u.state}')

  elif u.state == St.S15_SIXTY:
    u.state = St.S19_
    bot.send_message(msg.chat.id, iso5_2Net)
    if debug: bot.send_message(msg.chat.id,f'70:{u.state}')

  elif u.state == St.S14_OTHER:
    u.state = St.S19_
    bot.send_message(msg.chat.id, iso5_2Net)
    if debug: bot.send_message(msg.chat.id,f'82:{u.state}')

  elif u.state == St.S19_:
    #u.state = St.S19_
    bot.send_message(msg.chat.id, iso5_2Net)
    if debug: bot.send_message(msg.chat.id,f'87.7:{u.state}')

  elif u.state == St.S16_OTHER:
    u.state = St.S21_
    bot.send_message(msg.chat.id, f'כנס ל-5 ימי בידוד. בצע כעת בדיקת אנטיגן מוסדית במקרה שבוצעה בדיקה ביתית.{q_res}')
    if debug: bot.send_message(msg.chat.id,f'93:{u.state}')

  else:
    if debug: bot.send_message(msg.chat.id, f'עדיין לא מקודד. 96\n{u.state}')

@bot.message_handler(regexp='לא')
def hello(msg):
  u = get_user(msg.chat.id)
  if u.state == St.NAMED: #the NO response here is an answer to "exposed or not"
    u.state = St.S0_NOT_EXPOSED
    bot.send_message(msg.chat.id, "המשך יום נעים")  # this merely sends a message
    if debug: bot.send_message(msg.chat.id,f'104:{u.state}')

  elif u.state == St.S1_EXPOSED: #we are expecting his immuned or not answer
    u.state = St.S2_NOT_IMMUNE
    bot.send_message(msg.chat.id, q60)
    if debug: bot.send_message(msg.chat.id,f'109:{u.state}')

  elif u.state == St.S3_IMMUNE:
    u.state = St.S16_OTHER
    bot.send_message(msg.chat.id, aNoIso)
    if debug: bot.send_message(msg.chat.id,f'114:{u.state}')

  elif u.state == St.S16_OTHER:
    u.state = St.S22_
    bot.send_message(msg.chat.id, exempt)
    if debug: bot.send_message(msg.chat.id,f'119:{u.state}')

  elif u.state == St.S2_NOT_IMMUNE:
    u.state = St.S14_OTHER
    bot.send_message(msg.chat.id, aIso)
    if debug: bot.send_message(msg.chat.id,f'124:{u.state}')

  elif u.state == St.S14_OTHER:
    u.state = St.S18_
    bot.send_message(msg.chat.id, free)
    if debug: bot.send_message(msg.chat.id,f'129:{u.state}')

  elif u.state == St.S17_SIXTY:
    u.state = St.S22_
    bot.send_message(msg.chat.id, exempt)
    if debug: bot.send_message(msg.chat.id,f'134:{u.state}')
  elif u.state == St.S21_ or u.state == St.S19_:
    u.state = St.S26_
    bot.send_message(msg.chat.id, f'הנך חייב בבידוד 5 ימים. בצע בדיקת אנטיגן מוסדית במקרה שבוצעה בדיקה ביתית.{release}')
    if debug: bot.send_message(msg.chat.id,f'93:{u.state}')
  elif u.state == St.S26_:
    u.state = St.ANONYMOUS
    bot.send_message(msg.chat.id, f'אם יצאת שלילי ביום ה-5 וה-4 אתה משוחרר מבידוד.')
    if debug: bot.send_message(msg.chat.id,f'93:{u.state}')
  else:
    if debug: bot.send_message(msg.chat.id, f'עדיין לא מקודד. 137\n{u.state}')

@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(msg):
    # this is the standard reply to a normal message
    # it has to be used when user sends his name.
    # this type of default handler can mask other handlers. It must be located at the end.
    u = get_user(msg.chat.id)
    if u.state == St.UNKNOWN: #it's a brand new user
      u.state = St.ANONYMOUS
      bot.send_message(msg.chat.id, "הי, מה שמך?\nלהתחלה מחדש שלח  \n/help")
    elif u.state == St.ANONYMOUS: #already known:
      u.name = msg.text # take message as a name
      print(u.name, u.chat_id)
      u.state = St.NAMED
      bot.send_message(msg.chat.id, f'הי {u.name},\nהאם נחשפת?\nמשלב זה עליך לענות רק כן או לא!{st1}')
    else:
      #not sure why we are here. (Unhanled situation was reached)
      bot.send_message(msg.chat.id, f'הי, מצב לא נתמך 155.\n נסה שוב מאוחר יותר\n {u.state}\nלהתחלה מחדש שלח\n/help')

bot.polling()  # keeps the bot running and accepting messages