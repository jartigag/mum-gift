#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# RUN WITH:
# nohup python3 -u quetalvamichico_bot.py >> quetalvamichico_bot.log &

import urllib.request
import vobject
#import PyICU
#from change_tz import change_tz
#from datetime import datetime
from telegram import Bot, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

def message(text):
	bot = MyBot()
	bot.send_message(text)
	print(text)

class MyBot(Bot):
	def __init__(self, token='**123456789:tg-token**', chat_id='**987654321**'):
		Bot.__init__(self, token)
		self.chat_id = chat_id
	def send_message(self, text):
		super(MyBot, self).send_message(chat_id=self.chat_id, text=text, parse_mode=ParseMode.MARKDOWN)

def bold(text):
	return '*'+str(text)+'*'

def brackets(text):
	return '(_'+str(text)+'_)'

def from_to(start,end):
	#TODO2: return '\nsale: '+str(diasale)+' '+bold(horasale)+',\nllega: '+str(diasale)+' '+bold(horallega)
	return '\nsale: '+str(start)+',\nllega: '+str(end)

def doc_handler(bot, update):
	if update.effective_message.document.mime_type=='text/calendar':
		# Si se envían varios archivos a la vez, se queda con el último
		file = bot.getFile(update.effective_message.document.file_id)
		file.download('download.ics')

def bus_ics(file):
	with open(file, encoding="utf-8") as f:
		cal = vobject.readOne(f.read())
		descr = cal.vevent.summary.value
		dtstart = cal.vevent.dtstart.value #TODO3: parsear fecha (con bold(weekday))
		dtend = cal.vevent.dtend.value #TODO3: parsear fecha (con bold(weekday))
		#TODO2: tmstart, tmend
		return descr,dtstart,dtend#TODO2:,tmstart,tmend

def uni_ics(urlfile):
	with urllib.request.urlopen(urlfile) as u:
		cal = vobject.readOne(u.read().decode('utf8'))
		#TODO1: timezone
		#TODO1: change_tz(cal, PyICU.ICUtzinfo.getInstance('2'), PyICU.ICUtzinfo.getDefault())
		data = []
		#TODO1: cal.serialize(data)
		for vevent in cal.vevent_list:
			event = {'what':vevent.summary.value,'when':vevent.dtstart.value}
			data.append(event)
		return data

def tg_bus(bot, update):
	try:
		viaje, diasale, diallega = bus_ics('download.ics') #TODO: horasale, horallega
		message(bold(viaje)+from_to(diasale,diallega))
		#TODO2: from_to(diasale,horasale,diallega,horallega)
	except (IndexError, ValueError):
		update.message.reply_text("uso: /bus")

def tg_uni(bot, update):
	try:
		url = '**https://calendar.google.com/calendar/ical/aurlfromgooglecalendar/basic.ics**'
		data = uni_ics(url)
		for event in data:
			message(bold(event['what'])+' '+brackets(event['when']))
	except (IndexError, ValueError):
		update.message.reply_text("uso: /uni")

def main():
	updater = Updater(token='**123456789:tg-token**')
	dispatcher = updater.dispatcher
	dispatcher.add_handler(MessageHandler(Filters.document, doc_handler))
	dispatcher.add_handler(CommandHandler('uni', tg_uni))
	dispatcher.add_handler(CommandHandler('bus', tg_bus))
	updater.start_polling()
	updater.idle()

#TODO4: ping (avisa cuando llega a casa)

if __name__ == '__main__':
	main()
