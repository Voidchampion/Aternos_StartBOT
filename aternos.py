import discord
from discord.ext import commands, tasks
from playwright.async_api import async_playwright
import asyncio
import os

# ---------------- Bot Setup ----------------
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ---------------- Environment Variables ----------------
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
ATERNOS_EMAIL = os.getenv("ATERNOS_EMAIL")
ATERNOS_PASSWORD = os.getenv("ATERNOS_PASSWORD")

# Track server state
server_running = False

# ---------------- Helper Functions ----------------
async def login_aternos():
    """
    Returns a Playwright page logged into Aternos
    """
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=True)
    context = await browser.new_context()
    page = await context.new_page()
    
    # Go to Aternos login page
    await page.goto("https://aternos.org/go/")
    
    # Fill login form
    await page.fill('input[name="username"]', ATERNOS_EMAIL)
    await page.fill('input[name="password"]', ATERNOS_PASSWORD)
    await page.click('button[type="submit"]')
    
    # Wait for server page to load
    await page.wait_for_url("https://aternos.org/server/*", timeout=15000)
    
    return playwright, browser, context, page

async def start_server():
    global server_running
    playwright, browser, context, page = await login_aternos()
    
    try:
        await page.click('button:has-text("Start")')
        server_running = True
        return playwright, browser, context, page, True
    except:
        await browser.close()
        return playwright, browser, context, page, False

async def stop_server(page, browser):
    global server_running
    try:
        await page.click('button:has-text("Stop")')
        server_running = False
        await browser.close()
        return True
    except:
        await browser.close()
        return False

# ---------------- Commands ----------------
@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")

@bot.command()
async def start(ctx):
    global server_running
    if server_running:
        await ctx.send("⚠️ Server is already running!")
        return
    await ctx.send("🚀 Starting server...")
    
    result = await start_server()
    playwright, browser, context, page, success = result
    
    if success:
        await ctx.send("✅ Server started! Auto-stopping in 2 minutes.")
        # Auto-stop after 2 minutes
        await asyncio.sleep(120)
        stopped = await stop_server(page, browser)
        if stopped:
            await ctx.send("⏹️ Server stopped automatically.")
        else:
            await ctx.send("❌ Failed to stop server.")
    else:
        await ctx.send("❌ Failed to start server.")

@bot.command()
async def stop(ctx):
    await ctx.send("⚠️ Manual stop requires the page object, use !start first.")

# ---------------- Run Bot ----------------
bot.run(DISCORD_TOKEN)
