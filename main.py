import discord
from discord.ext import commands, tasks
from discord.utils import get
import random
from datetime import datetime
import pytz

id_server = 814789425790713887
id_logs_transac_channel = 817500492094767114
id_logs_ban_channel = 817905273514754088
id_logs_day_channel = 818608210364858378
id_logs_roulette_channel = 818116727074062346


default_intents = discord.Intents.default()
default_intents.members = True
bot = commands.Bot(command_prefix="!", intents=default_intents)


multi_double = 2
multi_chiffre = 5
multi_zero = 36

tz_NY = pytz.timezone('Europe/Paris')


@bot.event
async def on_ready():
    print("Ready !")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("faire le croupier !"))
    day_logs.start()


@bot.event
async def on_member_join(member):
    chanel_id = bot.get_channel(814798639477424199)
    pseudo = member.mention
    membre = member.guild.get_role(814789840524279838)
    await chanel_id.send(f"Nous souhaitons la bienvenue à {pseudo} qui vient de rejoindre le serveur !")
    await member.add_roles(membre)


@bot.command()
async def money(ctx, membre: discord.Member = None):
    channel = ctx.message.channel
    roles = ""
    if membre == None:
        roles = ctx.message.author.roles
    if membre != None:
        roles = membre.roles
    argent = ""

    for r in roles:
        if "$" in str(r):
            balance = str(r).split("$")
            money = balance[0]
            print(money)
            argent = f"{money}$"

    if channel.name == "『🏦』banque":

        if membre == None:
            embed = discord.Embed(
                title=("Balance :moneybag:"),
                description=(f"{ctx.message.author.mention}:\n\n{argent}"),
                colour=discord.Colour.red())
            await channel.send(embed=embed)

        if membre != None:
            embed = discord.Embed(
                title=("Balance :moneybag:"),
                description=(f"{membre.mention}:\n\n{argent}"),
                colour=discord.Colour.red())

            await channel.send(embed=embed)
    else:
        await ctx.message.delete()


@bot.command()
@commands.has_role('✨Employé✨')
async def set_money(ctx, member: discord.Member, money):
    roles = member.roles
    before_money = 0
    channel = ctx.message.channel
    guild = ctx.guild
    logs_chanel = bot.get_channel(id_logs_transac_channel)
    for r in roles:
        if "$" in str(r):
            balance = str(r).split("$")
            jetons = balance[0]
            before_money = jetons
            await r.delete()

    if channel.name == "『💳』transaction":
        role = await guild.create_role(name=f"{money}$ ({member.name})", color=discord.Colour(0xFF8B00))
        await member.add_roles(role)
        await channel.send(f"L'argent de  {member.mention} à bien était modifier !")
        await logs_chanel.send(f"L'argent de  {member.mention} est passer de {before_money}$ à {money}$ par {ctx.message.author.mention} !")

    else:
        await ctx.message.delete()

@bot.command()
@commands.has_role("Patron")
async def embed(ctx, title, *, texte):

    channel = ctx.message.channel

    embed = discord.Embed(
        title=(f"**{title}**"),
        description=(f"{texte}"),
        colour=discord.Colour.green())
    embed.set_thumbnail(url="https://mtxserv.com/forums/data/avatars/m/97/97936.jpg?1543645562")
    embed.set_footer(text="dev by GeniusTom#0450", icon_url="https://cdn.discordapp.com/avatars/353079782755401728/cecd76a85df5dbd1f4b3939c70468fda.png?size=256")
    await channel.send(embed=embed)
    await ctx.message.delete()


@bot.command()
@commands.has_role("✨Employé✨")
async def annonce(ctx, *, texte):
    channel = ctx.message.channel

    if channel.name == "『📢』annonces":
        await channel.purge(limit=10)
        embed = discord.Embed(
            description=(f"{texte}"),
            colour=discord.Colour.green())
        embed.set_footer(text="dev by GeniusTom#0450", icon_url="https://cdn.discordapp.com/avatars/353079782755401728/cecd76a85df5dbd1f4b3939c70468fda.png?size=256")
        await channel.send("@everyone", embed=embed)

        await ctx.message.delete()

@bot.command()
@commands.has_role("✨Employé✨")
async def open(ctx):
    channel = ctx.message.channel

    if channel.name == "『📢』annonce-dépôt-retrait":
        await channel.purge(limit=10)
        embed = discord.Embed(
            title="**Ouverture :white_check_mark:**",
            description=(f"Les dépots/retraits sont ouverts, dirigez vous vers un employer et dans le salon vocal: Attente de dépot !"),
            colour=discord.Colour.green())
        embed.set_image(url="https://media.discordapp.net/attachments/814867840569311252/834524507141308467/Capture_decran_rxr.png")
        embed.set_footer(text="dev by GeniusTom#0450", icon_url="https://cdn.discordapp.com/avatars/353079782755401728/cecd76a85df5dbd1f4b3939c70468fda.png?size=256")
        await channel.send("@everyone", embed=embed)

        await ctx.message.delete()
@bot.command()
@commands.has_role("✨Employé✨")
async def close(ctx):
    channel = ctx.message.channel

    if channel.name == "『📢』annonce-dépôt-retrait":
        await channel.purge(limit=10)
        embed = discord.Embed(
            title=(f"**Fermeture :x:**"),
            description=(f"Les dépots/retraits sont désormais fermer !"),
            colour=discord.Colour.green())
        embed.set_footer(text="dev by GeniusTom#0450", icon_url="https://cdn.discordapp.com/avatars/353079782755401728/cecd76a85df5dbd1f4b3939c70468fda.png?size=256")
        await channel.send("@everyone", embed=embed)

        await ctx.message.delete()

@bot.command()
@commands.has_role('✨Employé✨')
async def logs_days(ctx):
    guild = ctx.guild
    member = guild.members
    log_roulette = bot.get_channel(id_logs_roulette_channel)

    for m in member:
        for r in m.roles:
            if "$" in str(r):
                balance = str(r).split("$")
                jetons = balance[0]
                await log_roulette.send(f"L'utilisateur {m.mention} à {jetons}$")


@tasks.loop(seconds=5)
async def day_logs():

    guild = bot.get_guild(id_server)
    member = guild.members
    log_roulette = bot.get_channel(id_logs_day_channel)

    now = datetime.now(tz_NY)
    current_time = now.strftime("%H:%M:%S")
    minutes = ['00', '01', '02', "03", "04"]

    hour = current_time[0] + current_time[1]
    min = current_time[3] + current_time[4]
    sec = current_time[6] + current_time[7]


    if hour == "10" and min == "00" and sec in minutes:
        for m in member:
            for r in m.roles:
                if "$" in str(r):
                    jetons = str(r).split("$")
                    money = jetons[0]
                    if int(money) != 0:
                        await log_roulette.send(f"L'utilisateur {m.mention} à {money}$")



@bot.command()
@commands.has_role('✨Employé✨')
async def clear(ctx, amount=1):
    await ctx.message.delete()
    await ctx.channel.purge(limit=amount)

@bot.command()
@commands.has_role('✨Employé✨')
async def ban(ctx, membre: discord.Member,*,raison):
    channel = bot.get_channel(id_logs_ban_channel)
    pseudo = membre.mention
    await channel.send(f"Le joueur {pseudo} a été ban du serveur par {ctx.message.author} pour la raison :{raison}")
    await ctx.message.delete()
    await membre.ban()


@bot.command()
async def roulette(ctx, mise, pari):
    answer = random.randint(0, 36)
    roles = ctx.message.author.roles
    name = ""
    jetons = 0
    for r in roles:
        if "$" in str(r):
            name = str(r)
            balance = str(r).split("$")
            jetons = balance[0]
            jetons = int(jetons)

    role = discord.utils.get(ctx.message.guild.roles, name=name)
    logs_channel = bot.get_channel(id_logs_roulette_channel)
    server = bot.get_guild(id_server)
    channel = ctx.message.channel

    user = ctx.message.author
    mise = int(mise)

    money = 0

    jet = jetons - mise
    double = mise * multi_double
    fut_money_double = jet + double
    fut_money_double = round(fut_money_double)
    if fut_money_double < 0:
        fut_money_double = 0

    chiffre = mise * multi_chiffre
    fut_money_chiffre = jet + chiffre
    fut_money_chiffre = round(fut_money_double)
    if fut_money_chiffre < 0:
        fut_money_chiffre = 0

    zero = mise * multi_zero
    fut_money_zero = jet + zero
    fut_money_zero = round(fut_money_zero)
    if fut_money_zero < 0:
        fut_money_zero = 0


    if channel.name == "『🎲』roulette":

        if jetons == 0:
            await channel.send(f"{ctx.message.author.mention}, Vous n'avez pas de jetons !")

        elif mise > jetons:
            await channel.send(f"{ctx.message.author.mention}, Vous n'avez pas assez de jetons !")

        elif mise <= jetons:
            list_possible_bet = ['pair', 'impair', 'noir', 'rouge', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                                 '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23',
                                 '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36']

            list_numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16',
                            '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31',
                            '32', '33', '34', '35', '36']

            if pari in list_possible_bet:

                if pari == "pair" or pari == "impair":
                    resultat = (answer % 2)

                    if answer == 0:
                        await channel.send(f"Perdu la bille est tomber sur le zéro ! Vous perdez votre mise de {mise}$ {user.mention}")
                        await role.edit(name=f"{jet}$ ({user.name})")


                    else:

                        if resultat == 0:
                            if pari == "pair":
                                await role.edit(name=f"{fut_money_double}$ ({user.name})")
                                await channel.send(f"Bravo ! Le chiffre était {answer} il est donc {pari}! {user.mention}")


                            else:
                                await role.edit(name=f"{jet}$ ({user.name})")
                                await channel.send(f"Dommage ! Le chiffre était {answer} il est donc pair! Vous perdez votre mise de {mise}$ {user.mention}")
                        if resultat == 1:
                            if pari == "impair":
                                await role.edit(name=f"{fut_money_double}$ ({user.name})")
                                await channel.send(f"Bravo ! Le chiffre était {answer} il est donc {pari}! {user.mention}")
                            else:
                                await role.edit(name=f"{jet}$ ({user.name})")
                                await channel.send(f"Dommage ! Le chiffre était {answer} il est donc impair! Vous perdez votre mise de {mise}$ {user.mention}")


                if pari == "noir" or pari == "rouge":
                    resultat = (answer % 2)

                    if answer == 0:
                        await channel.send(f"Perdu la bille est tomber sur le zéro ! Vous perdez votre mise de {mise}$ {user.mention}")
                        await role.edit(name=f"{jet}$ ({user.name})")

                    else:
                        if resultat == 0:
                            if pari == "noir":
                                await role.edit(name=f"{fut_money_double}$ ({user.name})")
                                await channel.send(f"Bravo ! Le chiffre était {answer} il est donc {pari}! {user.mention}")
                            else:
                                await role.edit(name=f"{jet}$ ({user.name})")
                                await channel.send(f"Dommage ! Le chiffre était {answer} il est donc noir ! Vous perdez votre mise de {mise}$ {user.mention}")
                        if resultat == 1:
                            if pari == "rouge":
                                await role.edit(name=f"{fut_money_double}$ ({user.name})")
                                await channel.send(f"Bravo ! Le chiffre était {answer} il est donc {pari}! {user.mention}")
                            else:
                                await role.edit(name=f"{jet}$ ({user.name})")
                                await channel.send(f"Dommage ! Le chiffre était {answer} il est donc rouge! Vous perdez votre mise de {mise}$ {user.mention}")

                if pari in list_numbers:
                    if int(pari) == answer:
                        if int(pari) == 0:
                            await role.edit(name=f"{fut_money_zero}$ ({user.name})")
                            await channel.send(f"**Jackpot ! Vous multipliez votre mise par 36! {user.mention}**")
                        else:
                            await channel.send("**Winner ! Vous multipliez votre mise par 5! {user.mention}**")
                            await role.edit(name=f"{fut_money_chiffre}$ ({user.name})")
                    else:
                        await channel.send(f"Perdu c'était {answer}, vous perdez votre mise de {mise}$! {user.mention}")
                        await role.edit(name=f"{jet}$ ({user.name})")

    else:
        await user.send("Vous devez utilisez la commande dans le salon adéquat !")


print("Lancement du bot...")
bot_casino = "ODE0Nzg5MTY5NDc3NDUxODA3.YDi9jA.G25SMgxoDjellpyYyYMWhBZlzlY"
bot_croupier = "ODM1NDU4MzMyODYwMDg4MzMw.YIPvNA.hgbjJu7T3j6wOAbtAO106phe5n8"

bot.run(bot_croupier)

