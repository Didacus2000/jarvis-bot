import os
import discord
import threading
from flask import Flask
from discord.ext import commands
from groq import Groq

# 1. Configuración de Flask para "engañar" a Render
app = Flask(__name__)
@app.route('/')
def home():
    return "Jarvis está vivo"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# 2. Configuración del Bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Aquí iría tu lógica de Groq y eventos del bot...
# bot.run(os.environ['DISCORD_TOKEN'])

if __name__ == "__main__":
    # Iniciar la web en segundo plano
    t = threading.Thread(target=run_web)
    t.start()
    # Iniciar el bot
    bot.run(os.environ['DISCORD_TOKEN'])
