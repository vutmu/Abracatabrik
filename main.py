import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import redis

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

Messages = redis.from_url(os.environ.get("REDIS_URL"), db=0)
Messages.flushdb()

en = """qwertyuiop[]asdfghjkl;'zxcvbnm,./`QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?~)"""
ru = """йцукенгшщзхъфывапролджэячсмитьбю.ёЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё"""
en_layout = dict(zip(map(ord, en), ru))
ru_layout = dict(zip(map(ord, ru), en))
layout = {**ru_layout, **en_layout}


#
# bot = commands.Bot(command_prefix='>')
#
# @bot.command()
# async def ping(ctx):
#     await ctx.send('pong')
#
# bot.run(os.environ['TOKEN'])

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return
        else:
            if message.content == 'ping':
                await message.channel.send('pong')
            elif message.content in ('!tr', '!тр', '!nh', '!ек'):
                response = await translate(str(message.author))
                await message.channel.send(f'{str(message.author)}:{response}')
            else:
                # print(message.author, message.content)
                await load_to_db(str(message.author), str(message.content))


async def load_to_db(author, content):
    # if Messages.exists(author) == 1:
    #     print('тут надо добавить сообщение в список сообщений этого автора')
    # else:
    #     print('тут надо зарегать новый ключ автора и добавить туда сообщение')
    Messages.set(author, content, ex=30)


async def translate(author):
    message = Messages.get(author)
    if message:
        message = message.decode('utf-8')
        return message.translate(layout)
    else:
        return 'Ахалай-махалай!'


client = MyClient()
client.run(os.environ['TOKEN'])
