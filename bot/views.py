from django.shortcuts import render

__author__ = '@begyy'
from rest_framework.response import Response
from rest_framework.views import  APIView
from .models import Rates
import telebot
from django.conf import settings
from datetime import datetime, date, timedelta
import requests
from numpy import *
from matplotlib.pyplot import *


api_url = "https://api.exchangeratesapi.io/latest?base=USD"
api_url_history = "https://api.exchangeratesapi.io/history"
res = requests.get(api_url)
data = res.json()
time_update = datetime.now()

bot = telebot.TeleBot('927405192:AAETeWCBMhf9wLbgLSn_YRd1CqqyZn7ja9M')

class UpdateBot(APIView):
    def post(self,request):
        json_string = request.body.decode("UTF-8")
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])

        return Response({'code': 200})


# this function is used to update the database
# if there were no queries in the last 10 minutes.
def update_base(textrates, message):
    global time_update

    # fix the time of the last database update
    time_update = datetime.now()

    r = Rates.objects.all()
    r.delete()

    # show the result and save in the database
    for name, value in data['rates'].items():
        textrates += ('%s: %s %s' % (name, format(value, '.2f'), '\n'))
        r = Rates(name=name, value=value)
        r.save()
    bot.send_message(message.chat.id,textrates)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,'Write a chat "/" to see a list of commands\n'
                                   '/start - help text\n'
                                   '/list or /lst - returns list of all available rates\n'
                                   '/exchange $10 to CAD or  /exchange 10 USD to CAD - converts to \n'
                                   'the second currency with two decimal precision and return.\n'
                                   '/history USD/CAD for N days - return an image graph chart which\n'
                                   'shows the exchange rate graph/chart of the selected currency for the last N days.')


@bot.message_handler(commands=['list','lst'])
def show_list(message):
    textrates = ""
    if time_update < datetime.now()-timedelta(minutes=10):
        bot.send_message(message.chat.id, 'if')
        update_base(textrates, message)

    # if less than 10 minutes have passed, we take data from the database.
    else:
        bot.send_message(message.chat.id, 'else')
        for base in Rates.objects.all():
            textrates += ('%s: %s %s' % (base.name, base.value, '\n'))
        bot.send_message(message.chat.id,textrates)