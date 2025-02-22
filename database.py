import sqlite3

# Соединение с базой данных
database = sqlite3.connect('bot.sqlite')
cursor = database.cursor()

try:
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER,
            name TEXT,
            number INTEGER,
            personal_account INTEGER
        )
    ''')
    database.commit()
    print("Таблица 'users' создана (или уже существовала).")
except sqlite3.Error as e:
    print(f"Ошибка при создании таблицы: {e}")

# Функция для добавления пользователя
def add_user(message):
    cursor.execute("SELECT id FROM users WHERE id = ?", (int(message.chat.id),))
    user = cursor.fetchone()
    if not user:
        cursor.execute('INSERT INTO users VALUES (?, ?, ?, ?)', (message.chat.id, "name", 'number', "account"))
        database.commit()
    else:
        pass

# Функция для обновления имени пользователя
def add_user_name(message):
    cursor.execute("UPDATE users SET name = ? WHERE id=?", (message.text, message.chat.id,))
    database.commit()

# Функция для обновления номера пользователя
def add_user_number(message):
    cursor.execute("UPDATE users SET number = ? WHERE id=?", (message.text, message.chat.id,))
    database.commit()

# Функция для обновления номера лицевого счета
def add_user_personal_account(message):
    cursor.execute("UPDATE users SET personal_account = ? WHERE id=?", (message.text, message.chat.id))
    database.commit()

def is_user_registered(user_id):
    cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    return user is not None

def error_registration(user_id):
    try:
        cursor.execute("DELETE FROM users WHERE id =?", (user_id,))
        database.commit()
        print(f"Пользователь с ID {user_id} успешно удален из базы данных.")
    except sqlite3.Error as e:
        print(f"Ошибка при удалении пользователя с ID {user_id}: {e}")


# Не забудьте закрыть соединение, когда все операции будут завершены
# database.close()
