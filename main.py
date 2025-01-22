import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from aio_token import TOKEN
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.state import StatesGroup, State

bot = Bot(TOKEN)
dp = Dispatcher()

TEXT = """
/start - Запуск бота
/help - Справка
"""


# Класс для отслеживания состояний
class ConsultationState(StatesGroup):
    CHOOSING_TYPE = State()
    CHOOSING_SUB = State()


# Функция для создания клавиатуры
def create_keyboard(buttons, is_persistent=True, input_placeholder='Выберите вариант'):
    kb = [buttons] if not isinstance(buttons[0], list) else buttons
    return ReplyKeyboardMarkup(keyboard=kb, is_persistent=is_persistent, input_field_placeholder=input_placeholder,
                               one_time_keyboard=True, resize_keyboard=True)


# Функция для отправки сообщений при помощи клавиатуры
async def send_message_with_keyboard(message, text, buttons, state=None, is_persistent=True,
                                     input_placeholder="Выберите вариант"):
    keyboard = create_keyboard(buttons, is_persistent=is_persistent, input_placeholder=input_placeholder)
    await message.answer(text=text, reply_markup=keyboard)
    if state and isinstance(state, FSMContext): # Проверка типа state
        await state.set_state(state.state)

#Обработка команды /start
@dp.message(Command('start'))
async def on_start(message: types.Message, state: FSMContext):
    buttons = [
        [KeyboardButton(text='Консультация')],
        [KeyboardButton(text='Подбор оборудования УИРГ')],
        [KeyboardButton(text='Проектирование')],
        [KeyboardButton(text='Аккредитация УИРГ')]
    ]

    await send_message_with_keyboard(message,
                                     f'Приветствую {message.from_user.first_name} данный бот предназначен для помощи с УИРГ',
                                     buttons=buttons, is_persistent=True)

    await state.clear()

#Пользователь выбрал консультацию
@dp.message(F.text.lower() == 'консультация')
async def on_start_1(message: types.Message, state: FSMContext):
    buttons = [
        [KeyboardButton(text='Консультация по УИРГ')],
        [KeyboardButton(text='Другое')],
        [KeyboardButton(text='Назад в старт')]
    ]
    await send_message_with_keyboard(message, "Выберите тип консультации", buttons=buttons, is_persistent=True,
                                     state=ConsultationState.CHOOSING_TYPE)

#Пользователь вернулся на старт
@dp.message(F.text.lower() == 'назад в старт')
async def on_back_to_start(message: types.Message, state: FSMContext):
    buttons = [
        [KeyboardButton(text='Консультация')],
        [KeyboardButton(text='Подбор оборудования УИРГ')],
        [KeyboardButton(text='Проектирование')],
        [KeyboardButton(text='Аккредитация УИРГ')]
    ]

    await send_message_with_keyboard(message,
                                     f'Приветствую {message.from_user.first_name} данный бот предназначен для помощи с УИРГ',
                                     buttons=buttons)
    await state.clear()

#Пользователь выбрал консультацию по УИРГ
@dp.message(ConsultationState.CHOOSING_TYPE, F.text.lower() == 'консультация по уирг')
async def on_choice_1(message: types.Message, state: FSMContext):
    buttons = [
        [KeyboardButton(text='......'), KeyboardButton(text='......'), KeyboardButton(text='Назад'),
         KeyboardButton(text='Назад в старт')],

    ]
    await send_message_with_keyboard(message, 'Выберите подтип консультации', buttons=buttons,
                                     state=ConsultationState.CHOOSING_SUB)

#Пользователь выбрал вернуться назад
@dp.message(ConsultationState.CHOOSING_SUB, F.text.lower() == 'назад')
async def on_back_from_subtype(message: types.Message, state: FSMContext):
    buttons = [
        [KeyboardButton(text='Консультация по УИРГ')],
        [KeyboardButton(text='Другое')],
        [KeyboardButton(text='Назад в старт')]
    ]
    await send_message_with_keyboard(message, "Выберите тип консультации", buttons=buttons, is_persistent=True,
                                     state=ConsultationState.CHOOSING_TYPE)


@dp.message(ConsultationState.CHOOSING_TYPE, F.text.lower() == 'другое')
async def on_choice_2(message: types.Message, state: FSMContext):
    buttons = [
        [KeyboardButton(text='......'), KeyboardButton(text='......'), KeyboardButton(text='Назад')],
    ]
    await send_message_with_keyboard(message, 'Выберите подтип консультации', buttons=buttons,
                                     state=ConsultationState.CHOOSING_SUB)

#Обработка /help
@dp.message(Command('help'))
async def on_help(message: types.Message):
    await message.reply(TEXT)

#Постоянная работа кода, а также если пользователь будет спамить когда бот выключен, ничего не произойдет.
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
