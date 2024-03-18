from datetime import date, datetime, timedelta
from os import getenv

import httpx
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dateutil.parser import parse
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ChatType
from uvloop import install

install()
load_dotenv()

app = Client(
    'ruuffs_bot',
    api_id=getenv('TELEGRAM_API_ID'),
    api_hash=getenv('TELEGRAM_API_HASH'),
    bot_token=getenv('TELEGRAM_BOT_TOKEN')
)


def format_cardapio(result, campus):
    return f"""
            \tCardápio de {campus} 🏫\n
            🗓️ {result['dia']}
            🥗 {result['salada']}
            🥗 {result['salada1']}
            🥗 {result['salada2']}
            🍚 {result['graos']}
            🍙 {result['graos1']}
            🥫 {result['graos2']}
            🍟 {result['acompanhamento']}
            🥩 {result['mistura']}
            🥦 {result['mistura_vegana']}
            🍩 {result['sobremesa']}
            """


@app.on_callback_query()
async def callback(client, callback_query):
    pages = {
        'campus': {
            'chapeco': InlineKeyboardButton('Chapecó', callback_data='chapeco'),
            'realeza': InlineKeyboardButton('Realeza', callback_data='realeza'),
            'cerro_largo': InlineKeyboardButton('Cerro Largo', callback_data='cerro_largo'),
            'laranjeiras_do_sul': InlineKeyboardButton('Laranjeiras do Sul', callback_data='laranjeiras_do_sul'),
            'texto': 'Escolha o campus 🏫'
        },
        'chapeco': {
            'segunda': InlineKeyboardButton('Segunda', callback_data='0'),
            'terca': InlineKeyboardButton('Terça', callback_data='1'),
            'quarta': InlineKeyboardButton('Quarta', callback_data='2'),
            'quinta': InlineKeyboardButton('Quinta', callback_data='3'),
            'sexta': InlineKeyboardButton('Sexta', callback_data='4'),
            'anterior': InlineKeyboardButton('Voltar pro Campus', callback_data='campus'),
            'texto': 'Chapecó escolha o dia 📅'
        },
        'realeza': {
            'segunda': InlineKeyboardButton('Segunda', callback_data='0'),
            'terca': InlineKeyboardButton('Terça', callback_data='1'),
            'quarta': InlineKeyboardButton('Quarta', callback_data='2'),
            'quinta': InlineKeyboardButton('Quinta', callback_data='3'),
            'sexta': InlineKeyboardButton('Sexta', callback_data='4'),
            'anterior': InlineKeyboardButton('Voltar pro Campus', callback_data='campus'),
            'texto': 'Realeza escolha o dia 📅'
        },
        'cerro_largo': {
            'segunda': InlineKeyboardButton('Segunda', callback_data='0'),
            'terca': InlineKeyboardButton('Terça', callback_data='1'),
            'quarta': InlineKeyboardButton('Quarta', callback_data='2'),
            'quinta': InlineKeyboardButton('Quinta', callback_data='3'),
            'sexta': InlineKeyboardButton('Sexta', callback_data='4'),
            'anterior': InlineKeyboardButton('Voltar pro Campus', callback_data='campus'),
            'texto': 'Cerro Largo escolha o dia 📅'
        },
        'laranjeiras_do_sul': {
            'segunda': InlineKeyboardButton('Segunda', callback_data='0'),
            'terca': InlineKeyboardButton('Terça', callback_data='1'),
            'quarta': InlineKeyboardButton('Quarta', callback_data='2'),
            'quinta': InlineKeyboardButton('Quinta', callback_data='3'),
            'sexta': InlineKeyboardButton('Sexta', callback_data='4'),
            'anterior': InlineKeyboardButton('Voltar pro Campus', callback_data='campus'),
            'texto': 'Laranjeiras do Sul escolha o dia 📅'
        }
    }
    if callback_query.data in pages:
        page = pages[callback_query.data]
        txt = page.pop('texto')
        inline_markup = InlineKeyboardMarkup(
            [list(page.values())]
        )
        await callback_query.edit_message_text(txt, reply_markup=inline_markup)
    else:
        await callback_query.edit_message_text('**Aguarde, carregando cardapio 🔄 🔄 🔄**')
        campus = callback_query.message.text.split('escolha')[0].strip()
        result = httpx.get(
            f"https://ru-uffs-api.mascdriver.com.br/campus/{callback_query.message.text.split('escolha')[0].strip().lower()}/dia/{callback_query.data}",
            timeout=20).json()
        if 'cardapios' not in result:
            await callback_query.edit_message_text("Erro 🔥 🔥 🔥 🔥 \nInforme o @mascdriver 🧯 🧯 🧯")
        else:
            result = result['cardapios'][0]
            await callback_query.edit_message_text(format_cardapio(result, campus))


@app.on_message(filters.command('cardapio'))
async def callbacks(client, message):
    inline_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton('Cardápio 📃', callback_data='campus')
            ]
        ]
    )
    await message.reply('**Escolha uma opção 🔗 **', reply_markup=inline_markup)


@app.on_message(filters.command('projeto'))
async def projeto(client, message):
    inline_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton('URL 🔗', url='https://github.com/mascDriver/ruuffs_bot')
            ]
        ]
    )
    await message.reply('Projeto no GitHub 💻', reply_markup=inline_markup)


@app.on_message(filters.command('git'))
async def projeto(client, message):
    inline_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton('URL 🔗', url='https://github.com/mascDriver')
            ]
        ]
    )
    await message.reply('Meus projetos no GitHub 💻', reply_markup=inline_markup)


@app.on_message(filters.command('help') | filters.command('start'))
async def help_command(client, message):
    await message.reply(
        'Esse é o menu para pedir ajuda! 🆘🆘🆘🆘\n'
        'Use **/start** para iniciar o bot! 🤖\n'
        'Use **/help** para pedir ajuda! 🆘\n'
        'Use **/cardapio** para ver o cardápio 📃\n'
        'Use **/projeto** para ver o projeto no GitHub 💻\n'
        'Use **/bus** para ver o próximo bus 🚌\n'
        '**/git** para ver os projetos no GitHub 💻\n'
    )


# @app.on_message()
# async def messages(client, message):
#     await message.reply(f"Não entendi o {message.text} ❔❔❔")

async def job_cardapio():
    result = httpx.get(f"https://ru-uffs-api.mascdriver.com.br/campus/chapeco/dia/{date.today().weekday()}",
                       timeout=20).json()
    if 'cardapios' not in result:
        await app.send_message("@mascdriver", f'Erro no cardapio automatico em Chapeco dia :{date.today().weekday()}'
                                              f'Resul: {result}')
    else:
        await app.send_message("@computacaouffs", format_cardapio(result['cardapios'][0], 'Chapecó'))


@app.on_message(filters.command('bus'))
async def send_nextbus(client, message):
    if message.chat.type == ChatType.PRIVATE:
        horarios = httpx.post('http://beta.eagletrack.com.br/api/coletivos/linhas/listar/horarios',
                              data={'diaSemana': datetime.now().weekday() + 1, 'linha': 23}).json()
        nexts_origin = list(filter(lambda x: parse(x['hrhorario']).time() > (datetime.now() - timedelta(hours=3)).time(), horarios))
        nexts_destiny = list(filter(lambda x: parse(x['hrhorario']).time() > (datetime.now() - timedelta(hours=3, minutes=30)).time(), horarios))
        await message.reply(f'''
        Próximos 🚌 🚌 🚌 🚌
        
            Sai do terminal às 🕛 : 
        
{nexts_origin[0]["hrhorario"]} - {nexts_origin[0]["lidescricao"] }
{nexts_origin[1]["hrhorario"]} - {nexts_origin[1]["lidescricao"] if len(nexts_origin) > 1 else ''}
        ''' if nexts_origin else 'Nenhum onibus saindo do terminal à partir desse horario')

        if nexts_destiny and nexts_destiny[0] != nexts_origin[0]:
            await message.reply(f'''
Próximos 🚌 🚌 🚌 🚌 que podem estar chegando na UFFS
        
             Saiu do terminal às 🕛 : 
        
{nexts_destiny[0]["hrhorario"]} - {nexts_destiny[0]["lidescricao"]}
        ''')


scheduler = AsyncIOScheduler()
scheduler.add_job(job_cardapio, "cron", hour=11, minute=30, day_of_week='mon-fri')

scheduler.start()
app.run()
