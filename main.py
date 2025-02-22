import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import StateFilter
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

import logging
import re

from aio_token import TOKEN
from app.keyboard import *
from app.UserRegister import UserRegister
from database import *

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

TEXT = """
/start - Запуск бота
/help - Справка
/register - регистрация
"""

#Проверка на номер телефона
async def check_number(number, chat_id):
    if not re.match(r'^\+79\d{9}|89\d{9}$', number):
        await bot.send_message(chat_id, 'Введен некорректно номер телефона')
        return False
    return True

#Проверка на лицевой счет
async def check_account(number, chat_id):
    if not number.isdigit():
        await bot.send_message(chat_id, 'Введен некорректный лицевой счет')
        return False
    return True

#Проверка на строку
async def check_str(string, chat_id):
    if not re.match(r'^(?=.*[a-zA-Z])[a-zA-Z\s-]+|[а-яА-Я\s-]+$', string):
        await bot.send_message(chat_id, "некорректный ввод данных")
        return False
    return True


# Функция для отправки сообщений при помощи клавиатуры
async def send_message_with_keyboard(message, text, buttons, is_persistent=True,
                                     input_placeholder="Выберите вариант"):
    keyboard = create_keyboard(buttons, is_persistent=is_persistent, input_placeholder=input_placeholder)
    await message.answer(text=text, reply_markup=keyboard)


# Обработка команды /start
@dp.message(Command('start'))
async def on_start(message: types.Message):
    user_id = message.from_user.id
    if is_user_registered(user_id):
        await send_message_with_keyboard(message,
                                         f'Приветствую {message.from_user.first_name} данный бот предназначен для помощи с УИРГ',
                                         buttons=START_MENU, is_persistent=True)
    else:
        await message.answer("Вы не зарегистрированы. Для регистрации используйте команду /register")


@dp.message(Command("register"))
async def on_register(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    if is_user_registered(chat_id):
        await message.answer("Вы уже зарегистрированы. Используйте /start для доступа к меню.")
        return
    add_user(message)
    await bot.send_message(chat_id, "Введите ваше имя:")
    await state.set_state(UserRegister.name)


# Обработчик для получения имени
@dp.message(StateFilter(UserRegister.name))
async def add_name_(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    name = message.text
    if not await check_str(name, chat_id):
        return
    await state.update_data(name=name)
    add_user_name(message)
    await bot.send_message(chat_id, "Отправьте ваш номер:")
    await state.set_state(UserRegister.number)


# Обработчик для получения номера
@dp.message(StateFilter(UserRegister.number))
async def add_numb_(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    number = message.text
    if not await check_number(number, chat_id):
        return
    await state.update_data(number=number)
    add_user_number(message)
    await bot.send_message(chat_id, "Введите ваш лицевой счет:")
    await state.set_state(UserRegister.account)


@dp.message(StateFilter(UserRegister.account))
async def add_account_(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    account = message.text
    if not await check_account(account, chat_id):
        return
    add_user_personal_account(message)
    await state.update_data(personal_account=account)
    data = await state.get_data()
    name = data.get("name")
    number = data.get("number")
    await bot.send_message(chat_id, f'Регистрация успешно завершена! \n Ваше имя: {name} \n Номер: {number} \n '
                                    f'Номер вашего лицевого счет: {account} \n'
                                    f'нажмите /start')
    await state.clear()


# Пользователь выбрал консультацию
@dp.message(F.text.lower() == 'консультация')
async def on_start_1(message: types.Message):
    await send_message_with_keyboard(message, "Выберите тип консультации", buttons=KONSULTANT_MENU, is_persistent=True,
                                     )

@dp.message(F.text.lower() == 'ошибка при регистрации')
async def error(message: types.Message):
    chat_id = message.chat.id
    error_registration(chat_id)
    await bot.send_message(chat_id,'Необходимо пройти регистрацию /register')



# Пользователь вернулся на старт
@dp.message(F.text.lower() == 'назад в старт')
async def on_back_to_start(message: types.Message):
    await send_message_with_keyboard(message,
                                     f'Приветствую {message.from_user.first_name} данный бот предназначен для помощи с УИРГ',
                                     buttons=START_MENU)
    # await state.clear()


# Пользователь выбрал консультацию по УИРГ
@dp.message(F.text.lower() == 'консультация по уирг')
async def on_choice_1(message: types.Message):
    buttons = [
        [KeyboardButton(text='Подтип 1'), KeyboardButton(text='Подтип 2'), KeyboardButton(text='Назад'),
         KeyboardButton(text='Назад в старт')],

    ]
    await send_message_with_keyboard(message, 'Выберите подтип консультации', buttons=buttons,
                                     )


# Пользователь выбрал вернуться назад
@dp.message(F.text.lower() == 'назад')
async def on_back_from_subtype(message: types.Message):
    await send_message_with_keyboard(message, "Выберите тип консультации", buttons=KONSULTANT_MENU, is_persistent=True,
                                     )


@dp.message(F.text.lower() == 'другое')
async def on_choice_2(message: types.Message):
    buttons = [
        [KeyboardButton(text='Подтип 3'), KeyboardButton(text='Подтип 4'), KeyboardButton(text='Назад')],
    ]
    await send_message_with_keyboard(message, 'Выберите подтип консультации', buttons=buttons, is_persistent=True, )


# Обработка /help
@dp.message(Command('help'))
async def on_help(message: types.Message):
    await message.reply(TEXT)


# Постоянная работа кода, а также если пользователь будет спамить когда бот выключен, ничего не произойдет.
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped!")
