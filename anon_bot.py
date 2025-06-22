import discord
from discord.ext import commands, tasks
from flask import Flask
from threading import Thread
import requests
import os

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
PING_URL = os.getenv("PING_URL")

intents = discord.Intents.default()
intents.message_content = True
intents.dm_messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

app = Flask(__name__)

@app.route('/')
def index():
    return "✅ Bot is running!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

@tasks.loop(minutes=5)
async def ping():
    if PING_URL:
        try:
            requests.get(PING_URL)
        except Exception as e:
            print(f"❌ Ошибка пинга: {e}")

@bot.event
async def on_ready():
    print(f"✅ Бот запущен как {bot.user}")
    ping.start()

@bot.event
async def on_message(message):
    if isinstance(message.channel, discord.DMChannel) and not message.author.bot:
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            await channel.send(f"📩 **Анонимное сообщение:**\n{message.content}")
            await message.channel.send("✅ Отправлено анонимно.")

Thread(target=run_web).start()
bot.run(TOKEN)
