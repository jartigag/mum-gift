#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# EJECUTAR CON:
# nohup python3 quetalvamichico_bot.py >> quetalvamichico_bot.log &

#TODO: testar en condiciones reales

import urllib.request
import vobject
import locale
from datetime import datetime
from time import sleep
from telegram import Bot, ParseMode
from telegram.ext import Updater, CommandHandler
import subprocess
from threading import Thread

locale.setlocale(locale.LC_TIME, 'es_ES.utf8') # para tener 'lunes' en lugar de 'Monday'
tkn = '==123456789:tg-token-USER-BOT=='
bot = Bot(token=tkn)
bot.chat_id = '==998877665==' #user-chatId
myLocalIP = '==192.168.X.X=='
weekendOut = False

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
		#TODO: invertir orden (de evento más próximo a más lejano)
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
	print('[*] - '+datetime.now().strftime('%a, %d %b %Y %H:%M:%S'),text)

def bold(text):
	return '*'+str(text)+'*'

def brackets(text):
	return '(_'+str(text)+'_)'

def pinging():
	global weekendOut
	while True:
		p = subprocess.Popen(["ping", "-q", "-c", "3", myLocalIP], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		droppedPackets = p.wait()

		if not droppedPackets and weekendOut:
			print("[*] -",datetime.now().strftime('%a, %d %b %Y %H:%M:%S'),myLocalIP+" ha llegado a casa")
			message("ha llegado a casa")
			weekendOut = False
		sleep(10) # secs

def main():
	global weekendOut
	# @user_bot
	updater = Updater(token=tkn)
	updater.dispatcher.add_handler(CommandHandler('uni', tg_uni))
	updater.dispatcher.add_handler(CommandHandler('bus', tg_bus))

	print('[#] - '+datetime.now().strftime('%a, %d %b %Y %H:%M:%S')+' - init @user_bot')
	Thread(target=updater.start_polling).start()
	Thread(target=pinging).start()

	while True:
		viaje, dSale, hSale, hLlega = bus_ics('download.ics') # próximo viaje
		print(dSale, hSale)
		# si es más tarde de la hora de salida (el viaje es de ida a casa):
		if (datetime.now().day>=int(dSale[len(dSale)-6:len(dSale)-4]) and
		datetime.now().hour>=int(hSale[:1]) and	datetime.now().minute>=int(hSale[3:5])):
			weekendOut = True
			print("[*] -",datetime.now().strftime('%a, %d %b %Y %H:%M:%S'),"weekendOut =",weekendOut)
		sleep(300)

if __name__ == '__main__':
	main()
