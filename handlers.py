import aiogram.types
from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from db import cur, con

router = Router()
class NumbersCallbackFactory(CallbackData, prefix="sec"):
    action: str


@router.message(Command("start"))
async def echo(message: aiogram.types.Message):
    try:
        cur.execute("""INSERT INTO users(id, username) VALUES(?,?)""", (message.from_user.id, f'{message.from_user.username}'))
        con.commit()
    except:
        pass
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="Управление гаджетами"),
        KeyboardButton(text="Добавить гаджет"),
    )
    await message.answer('''
Добро пожаловать на бета-тест нашей системы безопасности
<b>DEU Security</b>
    ''', parse_mode="HTML", reply_markup=builder.as_markup(resize_keyboard=True))



@router.message(Command("get_all_cams"))
async def echo(message: aiogram.types.Message):
    try:
        count = 1
        cur.execute("""SELECT * FROM C WHERE ownerID = ?""", (message.from_user.id,))
        global f
        f = cur.fetchall()
        msg = "Вот список всех камер, которые привязаны к этому аккаунту:"
        for i in f:
            msg += f"\n<b>📹 Камера {count} (<a href=\"DEUSecurity.com/cams/{i[0]}\"><u>{i[0]}</u></a>)</b>"
            count += 1
        await message.answer(msg, parse_mode="HTML", disable_web_page_preview=True)
        
    except:
        pass
#     builder = ReplyKeyboardBuilder()
#     builder.row(
#         KeyboardButton(text="Управление гаджетами"),
#         KeyboardButton(text="Добавить гаджет"),
#     )
#     await message.answer('''
# Добро пожаловать на бета-тест нашей системы безопасности
# <b>DEU Security</b>
#     ''', parse_mode="HTML", reply_markup=builder.as_markup(resize_keyboard=True))


@router.message()
async def message_chek(message: aiogram.types.Message):
    if("Добавить гаджет" in message.text):
        await message.answer("""Введите код устройства, которй указан на его боковой стороне по форме: \"add_device КОД_ДЕВАЙСА-ТИП\"
Типы:
1. Камера - C
2. Свет - L
3. Дверь - D
4. Окно - W
5. Чайник - T
6. Пылесос - V                       

Пример: "add_device C27SJ2-C", для добавления Камеры
                             """)
    elif(message.text.split()[0] == "add_device"):
        arg = message.text.split()[1]
        arg = arg.split("-")
        argC = arg[0]
        argT = arg[1]
        messageD = await message.answer("Проверяю наличие кода в базе данных")
        cur.execute(f"SELECT * FROM {argT} WHERE deviceID = ?", (argC,))
        f = cur.fetchall()
        print(f)
        if f != []:
            if message.from_user.id == f[0][1]:
                await messageD.edit_text("Вы уже добавили это устройство")
            else:
                await messageD.edit_text("Это устройство уже добавлено другим пользователем")
            return
       
        try: 
            await messageD.edit_text("Добавляю устройство в базу данных")
            cur.execute(f"""INSERT INTO {argT}(deviceID, ownerID) VALUES(?,?)""", (argC, message.from_user.id))
            con.commit()
            await messageD.edit_text("Устройство успешно добавлено в базу данных")
        except:
            await messageD.edit_text("STOP")

@router.callback_query(NumbersCallbackFactory.filter())
async def handle_callbacks(callback: aiogram.types.CallbackQuery, data: NumbersCallbackFactory):
    if(data.action == "manage"):
        callback.answer("Hello")
    
    elif("manage" in data.action.split("_")):
        callback.answer("HE")
