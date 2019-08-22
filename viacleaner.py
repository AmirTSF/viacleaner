
from pyrogram import Filters
import time
import sqlite3
from pyrogram import Client, MessageHandler
import logging
import requests
from pyrogram import errors
import asyncio 
import config

bot = Client(
    "my_account1",
    api_id=348759,
    api_hash="5dc6f4b54b1985199b42a069a5745306",
    bot_token='TOKEN',
    workers=5,
)
conn = sqlite3.connect("mydatabase.db", check_same_thread = False)
cursor = conn.cursor()

bot.start()



bot.send_message(config.admin, 'Я был запущен! New V ')



@bot.on_message(Filters.command("stats"))
def stats(client, message):
	try:
		if message.chat.id == config.admin:
			cursor.execute('SELECT * FROM deleted_messages')
			num_messages = cursor.fetchall()
			bot.send_message(config.admin, 'Зарегистрировано удалённых сообщений в базе: <b>{}</b>'.format(len(num_messages)), parse_mode='HTML')
	except Exception as e:

		bot.send_message(config.admin, str(e))		





@bot.on_message(Filters.command("start"))
def start(client, message):
	try:
		bot.send_message(message.chat.id, config.ru_greet_text)
	except Exception as e:
		bot.send_message(config.admin, 'New exception! \n' + str(e))


@bot.on_message(Filters.text)
def text_deleter(client, message):
	try:
		if message.chat.type != 'private':
			if message.via_bot:
				chat = message.chat.id
				user = message.from_user.id
				r = bot.get_chat_member(chat, user)
				if r.status == 'admin' or r.status == 'creator':
					pass
				else:
					chat = message.chat.id
					text = message.text
					bot.delete_messages(chat, message.message_id)
					cursor.execute("INSERT INTO deleted_messages  VALUES (?, ?)", (chat, text))
					conn.commit()
	except Exception as e:
		bot.send_message(config.admin, 'New exception! \n' + str(e))
    			



@bot.on_message(Filters.media)
def media_deleter(client, message):
	try:
		if message.chat.type != 'private':
			if message.via_bot:
				chat = message.chat.id
				user = message.from_user.id
				r = bot.get_chat_member(chat, user)
				if r.status == 'admin' or r.status == 'creator':
					pass
				else:
					bot.delete_messages(message.chat.id, message.message_id)
					chat = message.chat.id
					text = message.text
					cursor.execute("INSERT INTO deleted_messages  VALUES (?, ?)", (chat, text))
					conn.commit()
	except Exception as e:
		bot.send_message(config.admin, 'New exception! \n' + str(e))


@bot.on_message(Filters.service)
def service_del(client, message):
	try:
		bot.delete_messages(message.chat.id, message.message_id)
	except Exception as e:
		bot.send_message(config.admin, str(e))
