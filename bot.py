import os
import discord
import threading
from flask import Flask
from discord.ext import commands
from groq import Groq
from androidtvremote2 import AndroidTVRemote
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
# --- Módulo de Control de TV ---
@bot.command()
async def tv(ctx, *, accion):
    await ctx.send(f"Jarvis ha recibido la orden para la TV: {accion}")
# Inicializar cliente de Groq
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
        if message.content.startswith('!'):
        await bot.process_commands(message)
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
# --- Módulo de Control de TV ---
@bot.command()
async def tv(ctx, *, accion):
    if accion == "conectar":
        # Esta lógica inicializará el cliente de Android TV Remote
        remote = AndroidTVRemote(TV_IP)
        # Aquí iniciaremos el proceso de emparejamiento
        await ctx.send("Iniciando emparejamiento. Revisa tu TV y escribe: !tv codigo [codigo_que_aparezca]")
    else:
        await ctx.send(f"Orden enviada: {accion}")
        
if __name__ == "__main__":
    # Iniciar la web en segundo plano
    t = threading.Thread(target=run_web)
    t.start()
    # Iniciar el bot
    bot.run(os.environ['DISCORD_TOKEN'])
