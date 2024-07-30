import disnake, os, Util
from disnake.ext import commands
from dotenv import load_dotenv
from typing import Final

# Edit These -----------------------------------------------

# Keep string within ''
captchastring = 'Example1'

# Input ID's
serverid = 0000000000000000000
outputchannelid = 0000000000000000000
subroleid = 0000000000000000000
domroleid = 0000000000000000000
switchroleid = 0000000000000000000
unverifiedroleid = 0000000000000000000

# Fetch Token - Change to however your hosting stores secrets
load_dotenv()
BOT_TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# -----------------------------------------------------------

# Bot initialization
command_sync_flags = commands.CommandSyncFlags.default()
command_sync_flags.sync_commands_debug = True
bot = commands.Bot(command_prefix='/', command_sync_flags=command_sync_flags)
guild = None

@bot.event
async def on_ready():
    await initializeguild()
    print(f"{bot.user} is now online")

@bot.event
async def on_guild_join(member):
    await member.add_roles(unverifiedrole, reason='Automatic Role Upon Joining', atomic=True)

async def initializeguild():
    global guild
    global serverid
    global subrole
    global domrole
    global switchrole
    global unverifiedrole
    global outputchannel
    guild = await bot.fetch_guild(serverid)
    subrole = guild.get_role(subroleid)
    domrole = guild.get_role(domroleid)
    switchrole = guild.get_role(switchroleid)
    unverifiedrole = guild.get_role(unverifiedroleid)
    outputchannel = bot.get_channel(outputchannelid)

# Autocomplete Role Input
autocompleteroles = ["Sub", 'Dom', "Switch", "None"]
async def autocomp_role(inter, user_input: str):
    return [lang for lang in autocompleteroles if user_input.lower() in lang]

@bot.slash_command(description="Enter Verification Code, Minecraft Username and Role")
async def verify(inter, verificationcode: str, minecraftusername: str, role: str = commands.Param(autocomplete=autocomp_role)):
    if verificationcode == captchastring:
        author = inter.author
        isverified = author.get_role(unverifiedroleid)
        if isverified != None:
            embed = Util.embed_builder(title='Successful Verification',
                                       description='Welcome to the server, please wait until an admin can whitelist you',
                                       author=author)
            outputembed = Util.embed_builder(title=f'New Verification For: {author} | <@{author.id}>',
                                             description=f'Command: /whitelist {minecraftusername}',
                                             author='AutoVerification')
            if role.lower() == "sub" or role.lower() == "submissive":
                await author.add_roles(subrole, reason='AutoVerification', atomic=True)
                await author.remove_roles(unverifiedrole, reason='AutoVerification', atomic=True)
                await inter.response.send_message(embed=embed, ephemeral=True)
                await outputchannel.send(embed=outputembed)
            elif role.lower() == "dom" or role.lower() == "dominant":
                await author.add_roles(domrole, reason='AutoVerification', atomic=True)
                await author.remove_roles(unverifiedrole, reason='AutoVerification', atomic=True)
                await inter.response.send_message(embed=embed, ephemeral=True)
                await outputchannel.send(embed=outputembed)
            elif role.lower() == "switch" or role.lower() == 'both':
                await author.add_roles(switchrole, reason='AutoVerification', atomic=True)
                await author.remove_roles(unverifiedrole, reason='AutoVerification', atomic=True)
                await inter.response.send_message(embed=embed, ephemeral=True)
                await outputchannel.send(embed=outputembed)
            elif role.lower() == 'None':
                await author.remove_roles(unverifiedrole, reason='AutoVerification', atomic=True)
                await inter.response.send_message(embed=embed, ephemeral=True)
                await outputchannel.send(embed=outputembed)
            else:
                embed = Util.embed_builder(title='Unsuccessful Verification', description='Please select a role from the list', author=author)
                await inter.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = Util.embed_builder(title='Unsuccessful Verification', description='You are already verified, use the roles channel to change role', author=author)
            await inter.response.send_message(embed=embed, ephemeral=True)

    else:
        embed = Util.embed_builder(title='Unsuccessful Verification', description='Incorrect verification code', author=inter.author)
        await inter.response.send_message(embed=embed, ephemeral=True)



# Start The Bot
bot.run(BOT_TOKEN)