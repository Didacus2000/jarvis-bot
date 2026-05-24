from flask import Flask
from threading import Thread

app = Flask('')
@app.route('/')
def home():
    return "Jarvis está vivo"

def run():
    port = int(os.environ.get("PORT", 10000)) # Esto toma el puerto de Render
    app.run(host='0.0.0.0', port=port)

t = Thread(target=run)
t.start()
import os
import discord
from discord.ext import commands
from groq import Groq

# Configuración de los "oídos" del bot
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Inicializar el cerebro (Groq)
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@bot.event
async def on_ready():
    print(f"J.A.R.V.I.S. está en línea y conectado como {bot.user}")
    # Cambia el estado en Discord
    await bot.change_presence(activity=discord.Game(name="Asistente de Didacus"))

@bot.event
async def on_message(message):
    # Evitar que el bot se responda a sí mismo
    if message.author == bot.user:
        return

    # Si nos hablan por privado o nos mencionan o escribimos en un canal
    # Activamos la respuesta inteligente de Groq
    async with message.channel.typing():
        try:
            response = groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "Eres J.A.R.V.I.S., el asistente de IA leal, eficiente y avanzado de Didacus. Responde de forma inteligente, concisa y con un toque elegante."},
                    {"role": "user", "content": message.content}
                ],
                model="llama3-8b-8192",
            )
            reply = response.choices[0].message.content
            await message.channel.send(reply)
        except Exception as e:
            await message.channel.send("Señor, experimenté un error al procesar su solicitud.")
            print(e)

    await bot.process_commands(message)

# Arrancar el bot usando el Token de Discord guardado en la nube
bot.run(os.getenv("DISCORD_TOKEN"))
