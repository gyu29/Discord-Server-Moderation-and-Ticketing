import discord
from discord.ext import commands

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)
token = ''

warnings = {}  # {user_id: warning_count}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message, member: discord.Member):
    if message.author.bot:
        return

    if any(word in message.content.lower() for word in ['n***a', 'p***']):
        user_id = str(message.author.id)
        warnings[user_id] = warnings.get(user_id, 0) + 1
        warning_count = warnings[user_id]

        if warning_count <= 2:
            await message.channel.send(f"{message.author.mention}, Warning {warning_count} out of 3. Please refrain from using heavy profanity.")

        if warning_count == 3:
            await message.channel.send(f"{message.author.mention}, Final Warning! One more warning and you will be timed-out for 1 hour.")
        
        if warning_count >= 4:
            await message.delete()
            await message.author.send("You have been timed-out for 1 hour due to multiple warnings.")
            await member.timeout(duration='3600', reason=f"Severe Profanity") 
            
    await bot.process_commands(message)

@bot.command()
async def status(ctx, user: discord.Member, *, status: str):
    embed = discord.Embed(title="Admin Status", description=f"Admin Availability", color=discord.Colour.blue())
    embed.add_field(name=f'{user}': {status})
    await ctx.send(embed=embed)

@bot.command()
async def ticket(ctx):
    embed = discord.Embed(title="Ticket", description="Press the button below to create a ticket.")
    button_label = "Create Ticket"
    view = discord.ui.View()
    view.add_item(discord.ui.Button(style=discord.ButtonStyle.green, label=button_label, custom_id="create_ticket"))
    await ctx.send(embed=embed, view=view)

@bot.command()
async def help(ctx):
    # Im too lazy to implement this shit
    pass

@bot.event
async def on_button_click(interaction):
    if interaction.custom_id == "create_ticket":
        user = interaction.user
        embed = discord.Embed(title="Ticket", description="Ticket has been created.", color=discord.Colour.green())
        await interaction.send(embed=embed, ephemeral=True)
        # Create and display the ticket channel with automated response

bot.run(token)
