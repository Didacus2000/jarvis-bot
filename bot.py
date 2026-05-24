import os
import discord
import threading
from flask import Flask
from discord.ext import commands
from groq import Groq

# 1. Configuración de Flask para Render
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

# Inicializar cliente de Groq
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    # Intentar obtener respuesta de Groq
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": message.content}],
            model="llama-3.3-70b-versatile",
        )
        response = chat_completion.choices[0].message.content
        await message.channel.send(response)
    except Exception as e:
        await message.channel.send(f"Error de conexión: {str(e)}")

if __name__ == "__main__":
    # Iniciar la web en segundo plano
    t = threading.Thread(target=run_web)
    t.start()
    # Iniciar el bot
    bot.run(os.environ['DISCORD_TOKEN'])
