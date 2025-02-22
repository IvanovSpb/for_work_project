from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

def create_keyboard(buttons, is_persistent=True, input_placeholder='Выберите вариант'):
    kb = [buttons] if not isinstance(buttons[0], list) else buttons
    return ReplyKeyboardMarkup(keyboard=kb, is_persistent=is_persistent, input_field_placeholder=input_placeholder,
                               one_time_keyboard=True, resize_keyboard=True)


START_MENU = [
    [KeyboardButton(text='Консультация'), KeyboardButton(text='Подбор оборудования УИРГ')],
    [KeyboardButton(text='Проектирование'), KeyboardButton(text='Аккредитация УИРГ')],
    [KeyboardButton(text='Ошибка при регистрации')]
]

KONSULTANT_MENU = [
        [KeyboardButton(text='Консультация по УИРГ')],
        [KeyboardButton(text='Другое')],
        [KeyboardButton(text='Назад в старт')]
    ]
