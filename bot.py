import discord
from discord.ext import commands
import os
import asyncio
from aternos import start_server, stop_server
from keep_alive import keep_alive

keep_alive()

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

shutdown_task = None

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")

@bot.tree.command(name="start", description="Start the Aternos server")
async def start(interaction: discord.Interaction):
    global shutdown_task

    await interaction.response.send_message("🚀 Starting server...")
    msg = start_server()
    await interaction.followup.send(msg)

    # Cancel existing shutdown timer
    if shutdown_task:
        shutdown_task.cancel()

    # Start new auto-shutdown timer
    shutdown_task = asyncio.create_task(auto_shutdown())

@bot.tree.command(name="stop", description="Stop the Aternos server")
async def stop(interaction: discord.Interaction):
    global shutdown_task

    if shutdown_task:
        shutdown_task.cancel()
        shutdown_task = None

    await interaction.response.send_message("🛑 Stopping server...")
    msg = stop_server()
    await interaction.followup.send(msg)

async def auto_shutdown():
    try:
        await asyncio.sleep(120)  # 2 minutes
        stop_server()
        print("🕒 Auto shutdown triggered")
    except asyncio.CancelledError:
        print("⏹ Auto shutdown cancelled")

bot.run(os.getenv("DISCORD_TOKEN"))
