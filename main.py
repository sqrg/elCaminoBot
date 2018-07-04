import configuration
import datetime
import discord
import sqlite3

from discord.ext import commands

votacion_abierta = False

conn = sqlite3.connect('elcamino.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS usuarios
             (id text, usuario text, agregado timestamp)''')

bot = commands.Bot(command_prefix='!', description='Desc')

@bot.event
async def on_ready():
    print('Logueado como')
    print(bot.user.name)

@bot.command()
async def iniciar():
    global votacion_abierta

    votacion_abierta = True
    await bot.say('Iniciar command')

@bot.command()
async def finalizar():
    global votacion_abierta

    votacion_abierta = False
    await bot.say('Finalizar command')

@bot.command()
async def listar():
    await bot.say('Listar command')

    c.execute('SELECT * FROM usuarios')
    participantes = c.fetchall()
    print(participantes)

@bot.command(pass_context=True)
async def quiero(ctx):
    global votacion_abierta

    if votacion_abierta:
        row_to_save = (ctx.message.author.id, ctx.message.author.display_name, ctx.message.timestamp)

        # Insert a row of data
        c.execute('INSERT INTO usuarios VALUES (?, ?, ?)', row_to_save)
        conn.commit()

        await bot.say('Agregado')

    else:
        await bot.say('No agregado')

bot.run(configuration.discord_bot_token)