import telegram

api_key = '5531979807:AAH6Jk92UkyuVpLc6qjBxfR_rVAK1cmBG3c'

bot = telegram.Bot(token = api_key)

chat_id = bot.get_updates()[-1].message.chat_id
print(chat_id)