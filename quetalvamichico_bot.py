#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# EJECUTAR CON:
# nohup python3 quetalvamichico_bot.py >> quetalvamichico_bot.log &

import urllib.request
import vobject
import locale
from datetime import datetime
from telegram import Bot, ParseMode
from telegram.ext import Updater, CommandHandler

locale.setlocale(locale.LC_TIME, 'es_ES.utf8') # para tener 'lunes' en lugar de 'Monday'
tkn = '==123456789:tg-token-USER-BOT=='
bot = Bot(token=tkn)
bot.chat_id = '==998877665==' #user-chatId

def tg_bus(bot,update):
	try:
		viaje, dSale, hSale, hLlega = bus_ics('download.ics')
		message(bold(viaje)+from_to(dSale,hSale,hLlega))
	except (IndexError, ValueError):
		update.message.reply_text("uso: /bus")

def tg_uni(bot,update):
	try:
		url = '==https://calendar.google.com/calendar/ical/A-URL-FROM-GOOGLE-CALENDAR/basic.ics=='
		data = uni_ics(url)
		for event in data:
			message(parse_event(event))
	except (IndexError, ValueError):
		update.message.reply_text("uso: /uni")

def bus_ics(file):
	with open(file, encoding="utf-8") as f:
		cal = vobject.readOne(f.read())
		descr = cal.vevent.summary.value
		dtstart = cal.vevent.dtstart.value
		dtend = cal.vevent.dtend.value

		dStart = dtstart.strftime("%A, %d %b")
		hStart = dtstart.strftime("%H:%M")
		hEnd = dtend.strftime("%H:%M")
		return descr,dStart,hStart,hEnd

def uni_ics(urlfile):
	with urllib.request.urlopen(urlfile) as u:
		cal = vobject.readOne(u.read().decode('utf8'))
		data = []
		for vevent in cal.vevent_list:
			event = {'what':vevent.summary.value,'when':vevent.dtstart.value}
			data.append(event)
		return data

def parse_event(event):
	what = event['what']
	when_str = str(event['when'])
	raw_when = datetime.strptime(when_str[:len(when_str)-6],'%Y-%m-%d %H:%M:%S')
	when = raw_when.strftime("%A, %d %b %H:%M")
	return bold(what)+' '+brackets(when)

def from_to(diaSale,horaSale,horaLlega):
	return '\nsale el '+bold(diaSale)+' a las '+bold(horaSale)+', llega a las '+horaLlega

def message(text):
	bot.send_message(chat_id = bot.chat_id, text=text, parse_mode=ParseMode.MARKDOWN)
	print('[*] - '+datetime.now().strftime('%a, %d %b %Y %H:%M:%S')+'\n'+text+'\n')

def bold(text):
	return '*'+str(text)+'*'

def brackets(text):
	return '(_'+str(text)+'_)'

def main():

	# @user_bot
	updater = Updater(token=tkn)
	updater.dispatcher.add_handler(CommandHandler('uni', tg_uni))
	updater.dispatcher.add_handler(CommandHandler('bus', tg_bus))

	print('[*] - '+datetime.now().strftime('%a, %d %b %Y %H:%M:%S')+' - init @user_bot')
	updater.start_polling()
	updater.idle()

#TODO: ping (avisa cuando llega a casa)

if __name__ == '__main__':
	main()
