#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# EJECUTAR CON:
# nohup python3 admin_qtvmc.py >> admin_qtvmc.log &

import urllib.request
import vobject
from datetime import datetime
from quetalvamichico_bot import bus_ics,from_to,message,bold
from telegram import Bot, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

tkn = '==123456789:tg-token-ADMIN-BOT=='
bot = Bot(token=tkn)
bot.chat_id = '==001122334==' #admin-chatId

def doc_handler(bot,update):
	if update.effective_message.document.mime_type=='text/calendar':
		# si se envían varios archivos a la vez, se queda con el último
		file = bot.getFile(update.effective_message.document.file_id)
		file.download('download.ics')
		viaje, dSale, hSale, hLlega = bus_ics('download.ics')
		message_check(bold(viaje)+from_to(dSale,hSale,hLlega))

def message_check(text):
	bot.send_message(chat_id = bot.chat_id, text=text, parse_mode=ParseMode.MARKDOWN)
	print('[*] - '+datetime.now().strftime('%a, %d %b %Y %H:%M:%S')+'\n'+text+'\n')

def msg(bot,update,args):
	try:
		# OJO: la función message es de @user_bot, así que los mensajes llegan allí
		message(update.message.text[4:]) # elimina '/msg '
		print('[>] - '+datetime.now().strftime('%a, %d %b %Y %H:%M:%S'),update.message.text)
	except (IndexError, ValueError):
		update.message.reply_text("uso: /msg <mensaje>")

def main():

	# @admin_bot
	updater = Updater(token=tkn)
	dispatcher = updater.dispatcher
	dispatcher.add_handler(MessageHandler(Filters.document, doc_handler))
	dispatcher.add_handler(CommandHandler('msg', msg, pass_args=True))

	print('[*] - '+datetime.now().strftime('%a, %d %b %Y %H:%M:%S')+' - init @admin_bot')
	updater.start_polling()
	updater.idle()

if __name__ == '__main__':
	main()
