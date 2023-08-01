import os
import telebot
from Eduserve import eduserve 
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

global user_id, password

dotenv_path = Path('D:\Code\Project\TT-bot\.env')
load_dotenv(dotenv_path=dotenv_path)

APIkey = os.getenv("APIkey")
bot = telebot.TeleBot(APIkey)

current_day = datetime.now().strftime("%a").upper()
day_map = {"MON":0, "TUE":1, "WED":2, "THR":3, "FRI":4}

def checkTime():
  this_year = int(datetime.now().strftime("%Y"))
  this_month =  int(datetime.now().strftime("%m"))
  this_day = int(datetime.now().strftime("%d"))

  if datetime.now() <= datetime(this_year, this_month, this_day, 9, 50, 00):
      return 0
  elif datetime(this_year, this_month, this_day, 9, 51, 00) <= datetime.now() <= datetime(this_year, this_month, this_day, 10, 45, 00):
      return 1
  elif datetime(this_year, this_month, this_day, 10, 46, 00) <= datetime.now() <= datetime(this_year, this_month, this_day, 11, 40, 00):
      return 2
  elif datetime(this_year, this_month, this_day, 11, 41, 00) <= datetime.now() <= datetime(this_year, this_month, this_day, 12, 45, 00):
      return 3
  elif datetime(this_year, this_month, this_day, 12, 46, 00) <= datetime.now() <= datetime(this_year, this_month, this_day, 2, 50, 00):
      return 4
  elif datetime(this_year, this_month, this_day, 2, 50, 00) <= datetime.now() <= datetime(this_year, this_month, this_day, 3, 45, 00):
      return 5
  elif datetime(this_year, this_month, this_day, 3, 45, 00) <= datetime.now() <= datetime(this_year, this_month, this_day, 4, 40, 00):
      return 6

@bot.message_handler(commands=['up'])
def up(message):
  sent = bot.send_message(message.chat.id, 'Username | Password')
  bot.register_next_step_handler(sent, hello)
def uprtcl(message):
  f = open(".env", "a")
  u,p = message.text.split(" ")
  f.write(f"\nLogin_ID={u}\nPassword={p}")
     
@bot.message_handler(commands=['login'])
def login(message):
  login_id = os.getenv("Login_ID")
  password = os.getenv("Password")
  print(login_id, password)
  obj = eduserve(login_id, password)
  obj.login()
  obj.getTimeTable()

@bot.message_handler(commands=['tday'])
def tday(message):
  f = open("Time_table.txt", "r")
  for i in range(5):
    if day_map[current_day] == i:
      lis = f.readline().split("|")
    f.readline() 
  x = "\n\n".join(lis)
  bot.send_message(message.chat.id ,x)  

@bot.message_handler(commands=['nowht'])
def nowht(message):
  f = open("Time_table.txt", "r")
  index = checkTime() 
  for i in range(5):
    if day_map[current_day] == i:
      lis = f.readline().split("|")
    f.readline()
  try:
    bot.send_message(message.chat.id ,lis[index])  
  except:
    bot.send_message(message.chat.id ,"No Class")

bot.polling()
