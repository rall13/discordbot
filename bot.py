import discord #модуль discord.py
from discord.ext import commands
import asyncio

#.help
client = commands.Bot( command_prefix = "." ) #Знак с помощью которого будут работать команды бота
#переменные
muted = 'mute'
#---------------------Events----------------------#
@client.event
#подключение
async def on_ready():
	print( 'Бот подключен by Rall' )

	await client.change_presence( status = discord.Status.online )
#welcome + выдача роли
@client.event
async def on_member_join( member ):


    emb = discord.Embed( description = f"Пользователь **{member.mention},** присоединился(-ась) к серверу!\n\n"
		f"Всего пользователей: {member.guild.member_count}\n\n",  color=0xff0000)

    role = discord.utils.get( member.guild.roles, id = 0 ) # ID роли которая будет выдаватся когда человек зашёл на сервер
    emb.set_thumbnail(url= member.avatar_url)
    emb.set_footer(icon_url= member.avatar_url)
    await member.add_roles( role )
    channel = client.get_channel( 0 ) # ID канала куда будет писатся сообщение (заменить 0 вашем ID)
    await channel.send( embed = emb )    
#----------------Команды----------------------------------#
#временный мут
@client.command(pass_context = True)
@commands.has_any_role('Название вашей роли', 0) #Вводите название вашей роли и её ID
async def tempmute(ctx, member: discord.Member = None, time: int = None, reason = None ):
	mute_role = discord.utils.get( ctx.message.guild.roles, name = muted )
	if member is None:
		await ctx.send(embed = discord.Embed(description = f'{ ctx.author.name }, **обязательно укажите (@Rall пример) пользователя!**', color = 0x4f4db3 ))
		await ctx.message.add_reaction( '❌' )
	else:
		if time is None:
			await ctx.send(embed = discord.Embed(description = f'{ ctx.author.name }, **обязательно укажите время (минуты)!**', color = 0x4f4db3 ))
			await ctx.message.add_reaction( '❌' )
		else:
			if mute_role is None:
				await ctx.send(embed = discord.Embed(description = f'{ ctx.author.name }, **обязательно создайте роль mute!**', color = 0x4f4db3 ))
				await ctx.message.add_reaction( '❌' )
			else:
				await member.add_roles(mute_role, reason = reason, atomic = True)
				await ctx.message.add_reaction( '✅' )
				await asyncio.sleep(time * 60)
				await member.remove_roles(mute_role)
#размут
@client.command()
@commands.has_any_role( 0 ) #ID вашей роли
async def unmute(ctx,member: discord.Member = None):
	mute_role = discord.utils.get( ctx.message.guild.roles, name = muted )
	if member is None:
		await ctx.send(embed = discord.Embed(description = f'❌{ ctx.author.name }, **обязательно укажите пользователя!**', color = 0x4f4db3 ))
		await ctx.message.add_reaction( '❌' )
	else:
		await member.remove_roles( mute_role )
		await ctx.message.add_reaction( '✅' )
#userinfo
@client.command()
async def userinfo(ctx, Member: discord.Member = None ):
    if not Member:
        Member = ctx.author
    roles = (role for role in Member.roles )
    emb = discord.Embed(title='Информация о пользователе.'.format(Member.name), description=f"Имя дискорда: {Member.name}\n\n"
		f"Никнейм на сервере: {Member.nick}\n\n"
		f"Статус: {Member.status}\n\n"
		f"ID: {Member.id}\n\n"
		f"Игрок присоединился к серверу: {Member.joined_at.strftime('%b %#d, %Y')}\n\n "
		f"Аккаунт создан: {Member.created_at.strftime('%b %#d, %Y')}", 
		color=0xff0000, timestamp=ctx.message.created_at)
    emb.set_thumbnail(url= Member.avatar_url)
    emb.set_footer(icon_url= Member.avatar_url)
    emb.set_footer(text='Команда вызвана: {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
    await ctx.send(embed=emb)
#avatar
@client.command()
async def avatar(ctx, member : discord.Member = None):
    user = ctx.message.author if (member == None) else member
    embed = discord.Embed(title=f'Аватар пользователя {user}', color= 0x0c0c0c)
    embed.set_image(url=user.avatar_url)
    await ctx.send(embed=embed)
#serverinfo
@client.command()
async def serverinfo(ctx, member: discord.Member = None):
    if not member:
        member = ctx.author

    guild = ctx.guild
    embed = discord.Embed(title=f"{guild.name}", description=f"Сервер создали {guild.created_at.strftime('%b %#d, %Y')}\n\n"
	f"Регион {guild.region}\n\n"
	f"Всего пользователей: {guild.member_count}\n\n",  color=0xff0000,timestamp=ctx.message.created_at)

    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.set_footer(text=f"ID: {guild.id}")
    embed.set_footer(text='Команда вызвана: {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
#ping 
@client.command()
async def ping(ctx, member: discord.Member = None ):
    await ctx.channel.purge(limit = 1)

    await ctx.send(embed = discord.Embed(
        title = '**🔴 Пинг бота**',
        description = f'**{client.ws.latency * 1000:.0f} мс**'
    ))

#connect (всегда в конце)
token = open ( 'token.txt', 'r' ).readline()

client.run ( token )