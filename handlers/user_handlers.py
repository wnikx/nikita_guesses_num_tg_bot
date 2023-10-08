from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.filters import Command, CommandStart
from lexicon.lexicon import LEXICON_RU
from aiogram import Router, F
import time

rt = Router()

ATTEMPTS = 7

user = {}

button_1 = KeyboardButton(text='⬆ Больше')
button_2 = KeyboardButton(text='Меньше ⬇')
button_3 = KeyboardButton(text='Хочу играть')
button_3_1 = KeyboardButton(text='Играть ещё')
button_4 = KeyboardButton(text='🎉 Угадал 🎉')
button_5 = KeyboardButton(text='Нет')

keyboard_1 = ReplyKeyboardMarkup(keyboard=[[button_3]], resize_keyboard=True)
keyboard_1_1 = ReplyKeyboardMarkup(
    keyboard=[[button_3_1]], resize_keyboard=True)
keyboard_2 = ReplyKeyboardMarkup(
    keyboard=[[button_1, button_2], [button_4]], resize_keyboard=True)
keyboard_3 = ReplyKeyboardMarkup(
    keyboard=[[button_4], [button_5]], resize_keyboard=True)


def find_number(start_num, end_num):
    start_num = (start_num + end_num) // 2
    return start_num


@rt.message(CommandStart())
async def process_command_start(message: Message):
    if message.from_user.id not in user:
        user[message.from_user.id] = {
            'in_game': False,
            'attempts': 0,
            'start_number': 50,
            'end_number': 100,
            'result': None,
            'lie': 0,
            'name': message.chat.first_name,
        }
    print(f'{message.chat.first_name}({message.from_user.id}) - захотел играть')
    if user[message.from_user.id]['in_game']:
        await message.answer(LEXICON_RU['in_game_player'])
    else:
        await message.answer(text=f'Хо-хо-хо, {user[message.from_user.id]["name"]}, рад встрече!\n'
                             'Правила просты, Вы загадывайте число от 0 до 99, а я его угадываю за 7 попыток!\n'
                             'Ваша задача говорить мне, больше оно или меньше, а когда угадаю, нажмите кнопку "Да" в чате.\n'
                             'Ну как, заманчиво?\n'
                             'Если всё устраивает давайте начнём, загадайте число и нажмите "Хочу играть".\n\n'
                             'Посмотреть полный список команд можно нажав - /help.', reply_markup=keyboard_1)


@rt.message(F.text.lower().in_(['старт', 'погнали', 'хочу играть', 'играть ещё']))
async def process_start_game(message: Message):
    if not user[message.from_user.id]['in_game']:
        user[message.from_user.id]['in_game'] = True
        user[message.from_user.id]['attempts'] += 1
        await message.answer(text=f'Дам вам пару секунд загадать число..', reply_markup=ReplyKeyboardRemove())
        time.sleep(3)
        await message.answer('Будьте честны, а то Никитка не станет с Вами играть!')
        time.sleep(3)
        await message.answer(f'И так начнём... Ваше число - {user[message.from_user.id]["start_number"]}?', reply_markup=keyboard_2)
        print(f'{message.chat.first_name}({message.from_user.id}) - начал играть')
    else:
        await message.answer(LEXICON_RU['in_game_player_1'])


@rt.message(F.text.lower().in_(['⬆ больше']))
async def process_greater_number(message: Message):
    if user[message.from_user.id]['lie'] >= 1:
        user[message.from_user.id]['lie'] += 1
        await message.answer('Хммм...')
        time.sleep(1)
        await message.answer('Мне кажется..кто-то врёт!')
        time.sleep(1)
        await message.answer(f'Напишите в чат угадал ли я Ваше число - {user[message.from_user.id]["result"]}?', reply_markup=keyboard_3)
    else:
        if user[message.from_user.id]['in_game']:
            if user[message.from_user.id]['result'] is None:
                result = (user[message.from_user.id]['end_number'] +
                          user[message.from_user.id]['start_number']) // 2
                user[message.from_user.id]['result'] = result
                await message.answer(f'Ваше число...{result}?')
            else:
                if user[message.from_user.id]['attempts'] > 6:
                    user[message.from_user.id]['lie'] += 1
                user[message.from_user.id]['start_number'] = user[message.from_user.id]['result']
                result = (user[message.from_user.id]['end_number'] +
                          user[message.from_user.id]['start_number']) // 2
                user[message.from_user.id]['result'] = result
                await message.answer(f'Ваше число...{result}?')
            user[message.from_user.id]['attempts'] += 1
        else:
            await message.answer(LEXICON_RU['in_game_player_1'])


@rt.message(F.text.lower().in_(['меньше ⬇']))
async def process_greater_number(message: Message):
    if user[message.from_user.id]['lie'] >= 1:
        user[message.from_user.id]['lie'] += 1
        await message.answer('Хммм...')
        time.sleep(1)
        await message.answer('Мне кажется..кто-то врёт!')
        time.sleep(1)
        await message.answer(f'Напишите в чат угадал ли я Ваше число - {user[message.from_user.id]["result"]}?', reply_markup=keyboard_3)
    else:
        if user[message.from_user.id]['in_game']:
            if user[message.from_user.id]['result'] is None:
                user[message.from_user.id]['end_number'] = user[message.from_user.id]['start_number']
                user[message.from_user.id]['start_number'] = 0
                result = (user[message.from_user.id]['end_number'] +
                          user[message.from_user.id]['start_number']) // 2
                user[message.from_user.id]['result'] = result
                await message.answer(f'Ваше число...{result}?')
            else:
                if user[message.from_user.id]['attempts'] > 6:
                    user[message.from_user.id]['lie'] += 1
                user[message.from_user.id]['end_number'] = user[message.from_user.id]['result']
                result = (user[message.from_user.id]['end_number'] +
                          user[message.from_user.id]['start_number']) // 2
                user[message.from_user.id]['result'] = result
                await message.answer(f'Ваше число...{result}?')
            user[message.from_user.id]['attempts'] += 1
        else:
            await message.answer(LEXICON_RU['in_game_player_1'])


@rt.message(F.text.lower().in_(['🎉 угадал 🎉', 'да', 'ага', "верно", "даа"]))
async def process_finish(message: Message):
    if user[message.from_user.id]['in_game']:
        print(f'{user[message.from_user.id]["name"]} - сыграл')
        print(f'{user[message.from_user.id]["result"]} - число которое загадал')
        print(f'{user[message.from_user.id]["attempts"]} - попытки')
        result_attempts = user[message.from_user.id]['attempts']
        user[message.from_user.id]['attempts'] = 0
        user[message.from_user.id]['in_game'] = False
        user[message.from_user.id]['start_number'] = 50
        user[message.from_user.id]['end_number'] = 100
        user[message.from_user.id]['result'] = None
        user[message.from_user.id]['lie'] = 0
        if result_attempts > 7:
            await message.answer(f'Великий маг Никитка снова сделал это, правда {user[message.from_user.id]["name"]} был не совсем честен!\n\n'
                                 "Если хотите сыграть ещё, нажмите 'Хочу играть'.\n\n"
                                 'Список всех комманд, можно получить нажав - /help', reply_markup=keyboard_1_1)
        else:
            await message.answer(f'Хах! {user[message.from_user.id]["name"]} Вы побеждены!\n'
                                 f'Великий маг Никитка снова сделал это, количeство попыток - {result_attempts}\n\n'
                                 "Если хотите сыграть ещё, нажмите 'Хочу играть'.\n\n"
                                 'Список всех команд, можно получить нажав - /help', reply_markup=keyboard_1_1)
    else:
        await message.answer(LEXICON_RU['other_words'])


@rt.message(Command(commands='cancel'))
async def process_command_cancel(message: Message):
    if user[message.from_user.id]['in_game']:
        print(f'{user[message.from_user.id]["name"]} - отказался')
        user[message.from_user.id]['attempts'] = 0
        user[message.from_user.id]['in_game'] = False
        user[message.from_user.id]['start_number'] = 50
        user[message.from_user.id]['end_number'] = 100
        user[message.from_user.id]['result'] = None
        user[message.from_user.id]['lie'] = 0
        await message.answer(LEXICON_RU['/cancel'], reply_markup=keyboard_1)
    else:
        await message.answer('Вы ещё не начали игру, чтобы сдаваться.\n'
                             'Нажмите /start, чтобы игра запустилась.\n\n'
                             'Список всех команд - /help')


@rt.message(F.text.lower().in_(['нет', 'не', 'неа',]))
async def process_command_refuse(message: Message):
    if user[message.from_user.id]['lie'] > 1:
        result_attempts = user[message.from_user.id]['attempts']
        user[message.from_user.id]['attempts'] = 0
        user[message.from_user.id]['in_game'] = False
        user[message.from_user.id]['start_number'] = 50
        user[message.from_user.id]['end_number'] = 100
        user[message.from_user.id]['result'] = None
        user[message.from_user.id]['lie'] = 0
        print(f'{user[message.from_user.id]["name"]} - обманул!')
        await message.answer(f'{user[message.from_user.id]["name"]}, я точно уверен, что Вы лукавите!')
        time.sleep(1)
        await message.answer('Вы исключайтесь из игры!', reply_markup=ReplyKeyboardRemove())
        time.sleep(1)
        await message.answer('Получить список всех комманд, можно нажав /help')
    else:
        if user[message.from_user.id]['in_game']:
            await message.answer('Напомню Вам, что надо написать "Больше" или "Меньше", тогда Никитка сможет угадать Ваше число.')
        else:
            await message.answer(LEXICON_RU['other_words'])


@rt.message(Command(commands='rules'))
async def process_command_rules(message: Message):
    await message.answer(LEXICON_RU['/rules'])


@rt.message(Command(commands='help'))
async def process_command_help(message: Message):
    await message.answer(LEXICON_RU['/help'])


@rt.message(Command(commands='owner'))
async def process_command_owner(message: Message):
    await message.answer('Создатель игры - самый-самый Никитка.')


@rt.message()
async def another_process(message: Message):
    if user[message.from_user.id]['in_game']:
        await message.answer('Вы в игре!\n'
                             "Продолжайте играть с Никиткой! Напишите больше, либо же меньше то число которое я Вам написал..\n\n"
                             "Если не хотите продолжать, напишите комманду /cancel")
    else:
        await message.answer(LEXICON_RU['other_words'])
