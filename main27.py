# for the different states and algorithm to implement see README.md.
# requires pyTelegramBotAPI package
import os
import telebot
from user import User, St

debug = False
st1='\nהבוט פועל לפי הנחיות מה-19/01'
q60='*האם אתה בן 60 ומעלה או נמצא בסיכון?*'
q_res = '\n*האם קיבלת תוצאה חיובית?*'
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

@bot.message_handler(commands=['debug'])  #this type of command will require user to type /Greet
def greet(message):
  global debug
  debug = not debug
  bot.reply_to(message, "Ok. toggling debug")  # this does a reply

@bot.message_handler(commands=['help']) #this vent triggers when user types /help
def help(message):   # we will use this as start over.
  u = get_user(message.chat.id)
  u.state = St.ANONYMOUS  # instead of defaulting to UNKNOWN
  bot.send_message(message.chat.id, "הי, מה שמך?\nלהתחלה מחדש שלח  \n/help")  # כאן מקובל להציג את מערכת הפקודות הנתמכת במערכת

@bot.message_handler(regexp='State')  # for debug purposes
def hello(msg):
  u = get_user(msg.chat.id)
  bot.send_message(msg.chat.id, u.state)  # this merely sends a message

@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(msg):
  # this type of default handler can mask other handlers. It must be located at the end.
  u = get_user(msg.chat.id)
  yesno=True
  if msg.text == 'כן':
    yes = True
  elif msg.text == 'לא':
    yes = False
  else: yesno=False
  ms = '' # the next message to send
  if yesno:  # handle all state changes for responses yes or no:
    if u.state == St.NAMED:  # the NO response here is an answer to "exposed or not"
      if yes: u.state, ms = St.S1_EXPOSED, "*האם הנך מחוסן (תו ירוק בתוקף)?*"
      else: u.state, ms = St.S0_NOT_EXPOSED, "המשך יום נעים"

    elif u.state == St.S1_EXPOSED:  # we are expecting his answer about immunity
      if yes: u.state, ms = St.S3_IMMUNE, q60
      else: u.state, ms = St.S2_NOT_IMMUNE, q60

    elif u.state == St.S3_IMMUNE: # expecting an answer about age.
      if yes: u.state, ms = St.S17_SIXTY, pNoIso
      else: u.state, ms = St.S16_OTHER, aNoIso

    elif u.state == St.S17_SIXTY: # expecting a test result
      if yes: u.state, ms = St.S23_, iso5_2Net
      else: u.state, ms = St.S22_, exempt

    elif u.state == St.S2_NOT_IMMUNE:
      if yes: u.state, ms = St.S15_SIXTY, pIso
      else: u.state, ms = St.S14_OTHER, aIso

    elif u.state == St.S15_SIXTY:
      if yes: u.state, ms = St.S19_, iso5_2Net
      else: u.state, ms = St.S20_, 'הנך נדרש להיכנס ל-5 ימי בידוד. \nשחרור לאחר בדיקת PCR שלילית שבוצעה ביום האחרון לבידוד'

    elif u.state == St.S14_OTHER:
      if yes: u.state, ms = St.S19_, iso5_2Net
      else: u.state, ms = St.S18_, free

    elif u.state == St.S16_OTHER:
      if yes: u.state, ms = St.S21_, f'כנס ל-5 ימי בידוד. בצע כעת בדיקת אנטיגן מוסדית במקרה שבוצעה בדיקה ביתית.{q_res}'
      else: u.state, ms = St.S22_, exempt

    elif u.state == St.S19_ or u.state == St.S21_ or u.state == St.S23_:
      if yes: ms = iso5_2Net
      # this looks like a BUG
      else: u.state, ms = St.S26_, f'הנך חייב בבידוד 5 ימים. בצע בדיקת אנטיגן מוסדית במקרה שבוצעה בדיקה ביתית.{release}'

  else: #handle some other responses.
    if u.state == St.UNKNOWN:
      u.state, ms = St.ANONYMOUS, "הי, מה שמך?\nלהתחלה מחדש שלח  \n/help"
    elif u.state == St.ANONYMOUS: #already known:
      u.name = msg.text # take message as a name
      print(f'name: {u.name}, first: {msg.chat.first_name}, last: {msg.chat.last_name}, user: {msg.chat.username}, chatid: {u.chat_id}')
      u.state, ms = St.NAMED, f'הי {u.name},\n*האם נחשפת?*\nמשלב זה עליך לענות רק\n*כן* או *לא*.{st1}'
    else:
      #not sure why we are here. (Unhanled situation was reached)
      ms = f'הי, מצב לא נתמך 155.\n נסה שוב מאוחר יותר\n {u.state}\nלהתחלה מחדש שלח\n/help'

  if debug:
    bot.send_message(msg.chat.id, f'{ms}\ncurrent state\n{u.state}')
  elif ms!='':
    bot.send_message(msg.chat.id, ms, parse_mode="markdown")


bot.polling()  # keeps the bot running and accepting messages