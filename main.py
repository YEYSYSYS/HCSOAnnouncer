import discord
from discord.ext import commands
from discord import app_commands
from keep_alive import keep_alive
import os

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
TOKEN = os.getenv("TOKEN")
GUILD_ID = os.getenv("GUILD_ID")

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    try:
        synced = await bot.tree.sync(guild=discord.Object(id=int(GUILD_ID))) if GUILD_ID else await bot.tree.sync()
        print(f"🔁 Synced {len(synced)} slash commands.")
    except Exception as e:
        print(f"❌ Sync error: {e}")

# Log every command usage
@bot.tree.command(name="botsay", description="Bot says what you type.")
@app_commands.describe(message="Message to say")
async def botsay(interaction: discord.Interaction, message: str):
    await interaction.response.send_message("✅ Sent!", ephemeral=True)
    await interaction.channel.send(message)
    print(f"{interaction.user} used /botsay: {message}")

@bot.tree.command(name="botembed", description="Create an embed message (Admins only)")
@app_commands.describe(
    title="Title of the embed",
    description="Main content of the embed",
    color="Color (hex, e.g. FF5733)",
    thumbnail="Thumbnail URL",
    image="Main image URL",
    field1_title="Field 1 title",
    field1_value="Field 1 value",
    field2_title="Field 2 title",
    field2_value="Field 2 value",
    field3_title="Field 3 title",
    field3_value="Field 3 value"
)
async def botembed(
    interaction: discord.Interaction,
    title: str,
    description: str,
    color: str = "2F3136",
    thumbnail: str = "",
    image: str = "",
    field1_title: str = "",
    field1_value: str = "",
    field2_title: str = "",
    field2_value: str = "",
    field3_title: str = "",
    field3_value: str = ""
):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ Admins only.", ephemeral=True)
        return

    embed = discord.Embed(title=title, description=description, color=int(color, 16))
    if thumbnail:
        embed.set_thumbnail(url=thumbnail)
    if image:
        embed.set_image(url=image)
    if field1_title and field1_value:
        embed.add_field(name=field1_title, value=field1_value, inline=True)
    if field2_title and field2_value:
        embed.add_field(name=field2_title, value=field2_value, inline=True)
    if field3_title and field3_value:
        embed.add_field(name=field3_title, value=field3_value, inline=True)

    await interaction.response.send_message("✅ Embed sent!", ephemeral=True)
    await interaction.channel.send(embed=embed)
    print(f"{interaction.user} used /botembed.")

### Simple Mod Tools (Admin Only)

@bot.tree.command(name="ban", description="Ban a user (Admins only)")
@app_commands.describe(user="User to ban", reason="Reason for ban")
async def ban(interaction: discord.Interaction, user: discord.Member, reason: str = "No reason provided"):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ Admins only.", ephemeral=True)
        return
    await user.ban(reason=reason)
    await interaction.response.send_message(f"🔨 Banned {user} for: {reason}")
    print(f"{interaction.user} banned {user} — {reason}")

@bot.tree.command(name="kick", description="Kick a user (Admins only)")
@app_commands.describe(user="User to kick", reason="Reason for kick")
async def kick(interaction: discord.Interaction, user: discord.Member, reason: str = "No reason provided"):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ Admins only.", ephemeral=True)
        return
    await user.kick(reason=reason)
    await interaction.response.send_message(f"👢 Kicked {user} for: {reason}")
    print(f"{interaction.user} kicked {user} — {reason}")

@bot.tree.command(name="clear", description="Clear messages (Admins only)")
@app_commands.describe(amount="Number of messages to delete")
async def clear(interaction: discord.Interaction, amount: int):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ Admins only.", ephemeral=True)
        return
    await interaction.channel.purge(limit=amount)
    await interaction.response.send_message(f"🧹 Cleared {amount} messages.", ephemeral=True)
    print(f"{interaction.user} cleared {amount} messages")

keep_alive()
bot.run(TOKEN)
