#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# RUN WITH:
# nohup python3 -u handler_qtvmc_bot.py >> handler_qtvmc_bot.log &

import urllib.request
import vobject
from datetime import datetime
from telegram import Bot, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

def message(text):
	bot = MyBot()
	bot.send_message(text)
	print('[*] - '+datetime.now().strftime('%a, %d %b %Y %H:%M:%S')+'\n'+text+'\n')

class MyBot(Bot):
	# @quetalvamichico_bot
	def __init__(self, token='**123456789:tg-token-main-bot**', chat_id='**987654321**'):
		Bot.__init__(self, token)
		self.chat_id = chat_id
	def send_message(self, text):
		super(MyBot, self).send_message(chat_id=self.chat_id, text=text, parse_mode=ParseMode.MARKDOWN)

def bold(text):
	return '*'+str(text)+'*'

def from_to(start,end):
	return '\nsale: '+str(start)+',\nllega: '+str(end)

def doc_handler(bot, update):
	if update.effective_message.document.mime_type=='text/calendar':
		# Si se envían varios archivos a la vez, se queda con el último
		file = bot.getFile(update.effective_message.document.file_id)
		file.download('download.ics')
		viaje, diasale, diallega = bus_ics('download.ics')
		message(bold(viaje)+from_to(diasale,diallega))

def bus_ics(file):
	with open(file, encoding="utf-8") as f:
		cal = vobject.readOne(f.read())
		descr = cal.vevent.summary.value
		dtstart = cal.vevent.dtstart.value
		dtend = cal.vevent.dtend.value
		return descr,dtstart,dtend

def msg(bot, update, args):
	try:
		message(update.message.text[4:]) #removes '/msg '
	except (IndexError, ValueError):
		update.message.reply_text("uso: /msg <mensaje>")

def main():
	# @handler_qtvmc_bot
	updater = Updater(token='**123456789:tg-token-handler-bot**')
	dispatcher = updater.dispatcher
	dispatcher.add_handler(MessageHandler(Filters.document, doc_handler))
	dispatcher.add_handler(CommandHandler('msg', msg, pass_args=True))
	print('[*] - '+datetime.now().strftime('%a, %d %b %Y %H:%M:%S')+' - init @handler_qtvmc_bot')
	updater.start_polling()
	updater.idle()

if __name__ == '__main__':
	main()
