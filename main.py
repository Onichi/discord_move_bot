import discord
from discord.ext import commands, tasks
from discord.utils import get
from config import config

voice_channel_list = []  # Fetch all channels from server

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


def fetchVoiceChannels():
    global voice_channel_list
    for guild in bot.guilds:
        for channel in guild.voice_channels:
            voice_channel_list.append(channel)

    print("Voice channels list:")
    [print(i, info) for i, info in enumerate(voice_channel_list)]



@bot.command(name="sta")  # Работает, создаёт новый канал и перемещает пользователя в него
async def starts(ctx):
    guild = ctx.guild
    member = ctx.author
    reference = guild.get_channel(1042096734651818054)
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False, connect=False),
        member: discord.PermissionOverwrite(view_channel=True, connect=True)
    }
    chanel = await guild.create_voice_channel("test", overwrites=overwrites, user_limit=2,
                                              position=reference.position + 1,
                                              category=reference.category, )
    await member.move_to(chanel)


@bot.event
async def on_voice_state_update(member, before, after):
    reference_channel = 1042165647825702932 #сюда id
    if after.channel is not None and after.channel.id == reference_channel:
        for guild in bot.guilds:
            reference = guild.get_channel(reference_channel)
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(view_channel=False, connect=False),
                member: discord.PermissionOverwrite(view_channel=True, connect=True)
            }
            chanel = await guild.create_voice_channel(member.name, overwrites=overwrites, user_limit=2,
                                                      position=reference.position + 1,
                                                      category=reference.category, )
            await member.move_to(chanel)
    elif after.channel is None and len(before.channel.members) == 0 and before.channel.id != 1042165647825702932: #и сюда
        await before.channel.delete()



@bot.command(name='clear')
@commands.has_permissions(manage_channels=True)
async def delete_empty_channels(ctx):
    guild = ctx.guild
    for channel in guild.voice_channels:
        if channel.category.id == 1042096602287984640 and channel.id != 1042165010153091103 and len(channel.members)==0: #сюда тоже
            await channel.delete()


bot.run(config['token'])
