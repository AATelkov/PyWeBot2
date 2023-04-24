import discord
import random
import requests
from bs4 import BeautifulSoup
import sqlalchemy as db
from discord import FFmpegPCMAudio
from config import token, video_cards, cpus, radio
from data import db_session
from data.users import User
from data.articles import Article
from discord.ext import commands

db_session.global_init("db/users_bot.db")

bot = commands.Bot(command_prefix="~", intents=discord.Intents.all())
bot.remove_command("help")
cansv = {}


def adding_a_user(autho_r, i_d):
    db_sess = db_session.create_session()

    if i_d not in [user.id_discord for user in db_sess.query(User).all()]:
        user = User()
        user.id_discord = i_d
        user.name = str(autho_r)
        db_sess.add(user)
        db_sess.commit()


def search_game(name):
    url = f"https://store.steampowered.com/search/?term={' '.join(name)}&category1=998"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        result = soup.select_one('.search_result_row')['href']
        return result
    except:
        return None


def search_for_components(element, accessories):
    acs = len(list(element))
    for i in accessories:
        for j in list(element):
            if j in i.split():
                acs -= 1
        if acs == 0 and i == " ".join(element):
            return i
        else:
            acs = len(list(element))
    else:
        return None


@bot.event
async def on_ready():
    db_session.global_init("db/users_bot.db")
    print("Бот в сети")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Играет в ~help"))


@bot.command()
async def author(ctx):
    await ctx.send(f"Мой создатель: Телков Антон#8518")


@bot.command()
async def game(ctx, *game):
    result = search_game(game)
    if not result:
        await ctx.channel.send("Игра не найдена")
    else:
        if "".join(game).lower() in result.lower().split("/") or "_".join(game).lower():
            await ctx.channel.send(result)
        else:
            await ctx.channel.send("Игра не найдена")


@bot.command()
async def add_completed_games(ctx, *games):
    db_sess = db_session.create_session()
    gm = ", ".join(" ".join(games).split(","))
    adding_a_user(ctx.author, ctx.author.id)
    if games:
        user = db_sess.query(User).filter(User.id_discord == int(ctx.author.id)).first()
        if user.completed_games:
            user.completed_games = user.completed_games + ", " + gm
        else:
            user.completed_games = gm
        db_sess.commit()
        await ctx.send(f"{ctx.author.name} добавил в пройденные игры: {gm}")
    else:
        await ctx.send("Что-то пошло не так")


@bot.command()
async def add_favorite_games(ctx, *games):
    db_sess = db_session.create_session()
    gm = ", ".join(" ".join(games).split(","))
    adding_a_user(ctx.author, ctx.author.id)
    if games:
        user = db_sess.query(User).filter(User.id_discord == int(ctx.author.id)).first()
        if user.favorite_games:
            user.favorite_games = user.favorite_games + ", " + gm
        else:
            user.favorite_games = gm
        db_sess.commit()
        await ctx.send(f"{ctx.author.name} добавил в избранные игры: {gm}")
    else:
        await ctx.send("Что-то пошло не так")


@bot.command()
async def search(ctx, *name):
    db_sess = db_session.create_session()
    nm = ", ".join(" ".join(name).split(","))
    user = db_sess.query(User).filter(User.name == str(ctx.author)).first()
    if user:
        if user.name == str(nm) and user.favorite_games or user.completed_games:
            await ctx.send(user.name[:-5])
            if user.favorite_games:
                await ctx.send(f"Избранные игры: {user.favorite_games}")

            if user.completed_games:
                await ctx.send(f"Завершённые игры: {user.completed_games}")
        else:
            await ctx.send("Введено некорректное имя или данный пользователь не зарегистрирован.")
    else:
        await ctx.send("Введено некорректное имя или данный пользователь не зарегистрирован.")


@bot.command()
async def add_video_card(ctx, *video_card):
    vc = search_for_components(video_card, video_cards)
    db_sess = db_session.create_session()
    adding_a_user(ctx.author, ctx.author.id)
    if vc:
        user = db_sess.query(User).filter(User.id_discord == int(ctx.author.id)).first()
        print(video_cards.index(vc))
        user.video_card = video_cards.index(vc)
        db_sess.commit()
        await ctx.send(f"{vc} сохранено и будет использоваться для поиска и создания записей.")
    else:
        await ctx.send("Что-то пошло не так")


@bot.command()
async def add_cpu(ctx, *cpu):
    vc = search_for_components(cpu, cpus)
    db_sess = db_session.create_session()
    adding_a_user(ctx.author, ctx.author.id)
    if vc:
        user = db_sess.query(User).filter(User.id_discord == int(ctx.author.id)).first()
        user.cpu = cpus.index(vc)
        db_sess.commit()
        await ctx.send(f"{vc} сохранено и будет использоваться для поиска и создания записей.")
    else:
        await ctx.send("Что-то пошло не так")


@bot.command()
async def add_ram(ctx, *ram):
    ram = int(ram[0])
    db_sess = db_session.create_session()
    if 1 <= ram <= 128:
        user = db_sess.query(User).filter(User.id_discord == int(ctx.author.id)).first()
        user.ram = ram
        db_sess.commit()
        await ctx.send(f"{ram}GB сохранено и будет использоваться для поиска и создания записей.")
    else:
        await ctx.send("Что-то пошло не так")


@bot.command()
async def article_creation(ctx, *args):
    game, fps = list(args)[0], int(list(args)[1])
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id_discord == int(ctx.author.id)).first()
    flag = True
    if user:
        if not user.video_card:
            await ctx.send("Укажите видеокарту с помощью команды '~add_video_card'")
            flag = False
        if not user.cpu:
            await ctx.send("Укажите процессор с помощью команды '~add_cpu'")
            flag = False
        if not user.ram:
            await ctx.send("Укажите оперативную память с помощью команды '~add_ram'")
            flag = False
        if flag:
            if 0 < fps < 1000:

                article = Article()
                article.games = game
                article.video_card = user.video_card
                article.cpu = user.cpu
                article.ram = user.ram
                article.fps = fps
                db_sess.add(article)
                db_sess.commit()
                await ctx.send("Сохранено успешно")
            else:
                await ctx.send("Неверный fps")
    else:
        await ctx.send("Что-то пошло не так")


@bot.command()
@commands.has_permissions(administrator=True)
async def clear(ctx):
    await ctx.channel.purge(limit=1000)


@bot.command()
async def play(ctx):
    if ctx.message.author.voice:
        cansv[ctx.message.author.voice.channel.id] = 0
        vs = await ctx.message.author.voice.channel.connect()
        vs.play(discord.FFmpegPCMAudio(radio[cansv[ctx.message.author.voice.channel.id]]))


@bot.command()
async def stop(ctx):
    if ctx.message.author.voice:
        cansv.pop(ctx.message.author.voice.channel.id)
        discord.utils.get(bot.voice_clients, guild=ctx.guild).stop()
        await discord.utils.get(bot.voice_clients, guild=ctx.guild).disconnect()


@bot.command()
async def sk(ctx):
    if ctx.message.author.voice:
        if cansv[ctx.message.author.voice.channel.id] + 1 == len(radio):
            cansv[ctx.message.author.voice.channel.id] = 0
        else:
            cansv[ctx.message.author.voice.channel.id] += 1
        discord.utils.get(bot.voice_clients, guild=ctx.guild).stop()
        discord.utils.get(bot.voice_clients, guild=ctx.guild) \
            .play(discord.FFmpegPCMAudio(radio[cansv[ctx.message.author.voice.channel.id]]))


@bot.command()
async def help(ctx):
    emb = discord.Embed(title="Команды")
    emb.add_field(name='author', value='Автор бота')
    emb.add_field(name='add_completed_games', value='Добавление завершенных игр')
    emb.add_field(name='add_favorite_games', value='Добавление пройденных игр')
    emb.add_field(name='search', value="Поиск по имени")
    emb.add_field(name='add_video_card', value="Добавление видеокарты")
    emb.add_field(name='add_cpu', value="Добавление процессора")
    emb.add_field(name='add_ram', value="Добавление оперативной памяти")
    emb.add_field(name='article_creation', value="Создание поста")
    emb.add_field(name='clear', value="Очистка чата")
    emb.add_field(name='game', value="Найти игру в Steam")
    emb.add_field(name='play', value="Включить радио")
    emb.add_field(name='sk', value="Переключить радио")
    emb.add_field(name='stop', value="Выключить радио")
    await ctx.send(embed=emb)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith("Бросить кубик"):
        await message.channel.send("Выпало число: " + str(random.randint(1, 6)))

    if message.content.lower() in ["во что бы поиграть", "подходящие игры"]:
        gems = {}
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id_discord == int(message.author.id)).first()
        if user:
            for article in db_sess.query(Article).all():
                if article.fps >= 30 and user.video_card <= article.video_card \
                        and user.cpu <= article.cpu and user.ram >= article.ram:
                    if article.games not in gems:
                        gems[article.games] = str(article.fps)
                    else:
                        gems[article.games] += ", " + str(article.fps)
            await message.channel.send(", ".join([i + " - (" + gems[i] + ")" for i in gems]))
        else:
            await message.channel.send("Вы не сохранили нужные данные")

    if message.content.lower() in ['камень', 'бумага', 'ножницы']:
        choices = ['камень', 'бумага', 'ножницы']
        bot_choice = random.choice(choices)
        player_choice = message.content.lower()

        if player_choice == bot_choice:
            await message.channel.send(f"Мы оба выбрали {player_choice}")
        elif player_choice == "камень":
            if bot_choice == "бумага":
                await message.channel.send(f"{bot.user.name} выигрывает! я выбрал {bot_choice}")
            else:
                await message.channel.send(
                    f"{message.author.name} выигрывает! Вы выбрали {player_choice}, а я выбрал {bot_choice}")
        elif player_choice == "бумага":
            if bot_choice == "ножницы":
                await message.channel.send(f"{bot.user.name} выигрывает! я выбрал {bot_choice}")
            else:
                await message.channel.send(
                    f"{message.author.name} выигрывает! Вы выбрали {player_choice}, а я выбрал {bot_choice}")
        else:
            if bot_choice == "камень":
                await message.channel.send(f"{bot.user.name} выигрывает! я выбрал {bot_choice}")
            else:
                await message.channel.send(
                    f"{message.author.name} выигрывает! Вы выбрали {player_choice}, а я выбрал {bot_choice}")

    if message.content.lower()[:3] == "бот":
        await message.channel.send(random.choice(["Я не могу понять ваше сообщение",
                                                  "Вызови ~help и посмотри, что я могу",
                                                  "Я не могу на это ответить",
                                                  "Я не знаю этого"]))
    await bot.process_commands(message)


if __name__ == "__main__":
    bot.run(token)
