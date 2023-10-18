from aiogram import types, F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from db import cur, con

router = Router()

database = ""


class MyCallback(CallbackData, prefix="my"):
    foo: str
    bar: int

class globalHandlers():
    @router.message(Command("start"))
    async def start_handler(msg: Message):
        try:
            cur.execute("""INSERT INTO users(id, username) VALUES(?,?)""", (msg.from_user.id, msg.from_user.username))
            con.commit()
        except:
            pass
        builder = ReplyKeyboardBuilder()
        builder.row(
        types.KeyboardButton(text="➕ Добавить девайс"),
        types.KeyboardButton(text="🔧 Управление девайсами")
        )
        await msg.answer('''
Здравствуйте, вас приветствует компания <b>DEU Security</b>
Снизу появилось меню управления ботом, если вы используете его впервые, нажмите на "Добавить девайс"
''', parse_mode="HTML",reply_markup=builder.as_markup(resize_keyboard=True))
        
    @router.message()
    async def check_message(message: Message):
        print(message.text)
        if("Управление девайсами" in message.text):
            # Создаем объекты инлайн-кнопок
            
            builder = InlineKeyboardBuilder()
            builder.row(
                types.InlineKeyboardButton(
            text="📹 Камеры",
            callback_data=MyCallback(foo="manage_Cameras", bar="42").pack()),
            types.InlineKeyboardButton(
            text="🌞 Свет",
            callback_data=MyCallback(foo="manage_Lights", bar="42").pack())
            ),
            builder.row(
                types.InlineKeyboardButton(
            text="🔐 Двери",
            callback_data=MyCallback(foo="manage_Doors", bar="42").pack()),
            types.InlineKeyboardButton(
            text="🔌 Другие девайсы",
            callback_data=MyCallback(foo="manage_Other devices", bar="42").pack())
            ),
            await message.answer(
                "<b>Выберите категорию, которой вы хотите управлять</b>",
                parse_mode="HTML",
                reply_markup=builder.as_markup()
            )
        if("Добавить девайс" in message.text):
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


    
        
   
class userHandlers():
    pass


class adminHandlers():
    pass


class callbacks():
    @router.callback_query(MyCallback.filter())
    async def my_callback_foo(query: CallbackQuery, callback_data: MyCallback):
        if("manage" in callback_data.foo):
            callback_data = callback_data.foo.split("_")
            if(callback_data[1] == "Cameras"):
                try:
                    count = 1
                    #getting from database
                    cur.execute("""SELECT * FROM C WHERE ownerID = ?""", (query.from_user.id,))
                    f = cur.fetchall()
                    print(f"FF: {f}")
                    if f == []:
                        await query.message.answer("Вы еще не добавили ни одной камеры")
                        return
                    msg = "Вот список всех камер, которые привязаны к этому аккаунту:"
                    builder = InlineKeyboardBuilder()
                    
                    for i in f:
                        builder.add(
                            types.InlineKeyboardButton(
                        text=f"📹 Камера {count}",
                        url=f"http://DEUSecurity.com/cams/{i[0]}")
                        )
                        # msg += f"\n<b>📹 Камера {count} (<a href=\"DEUSecurity.com/cams/{i[0]}\"><u>{i[0]}</u></a>)</b>"
                        count += 1
                    await query.message.answer(msg, parse_mode="HTML", disable_web_page_preview=True, reply_markup=builder.as_markup())
                except:
                    pass
            elif(callback_data[1] == "Lights"):
                try:
                    count = 1
                    #getting from database
                    cur.execute("""SELECT * FROM L WHERE ownerID = ?""", (query.from_user.id,))
                    f = cur.fetchall()
                    if f == []:
                        await query.message.answer("Вы еще не добавили ни одной лампы")
                        return
                    msg = "Вот список всех ламп, которые привязаны к этому аккаунту:"
                    builder = InlineKeyboardBuilder()
                    for i in f:
                        builder.add(
                            types.InlineKeyboardButton(
                        text=f"🌞 Лампа {count}", callback_data="turn_light")
                        
                        )
                        # msg += f"\n<b>📹 Камера {count} (<a href=\"DEUSecurity.com/cams/{i[0]}\"><u>{i[0]}</u></a>)</b>"
                        count += 1

                    await query.message.answer(msg, parse_mode="HTML", reply_markup=builder.as_markup())
                except:
                    pass
            elif(callback_data[1] == "Doors"):
                try:
                    count = 1
                    #getting from database
                    cur.execute("""SELECT * FROM D WHERE ownerID = ?""", (query.from_user.id,))
                    f = cur.fetchall()
                    if f == []:
                        await query.message.answer("Вы еще не добавили ни одной двери")
                        return
                    msg = "Вот список всех дверей, которые привязаны к этому аккаунту:"
                    builder = InlineKeyboardBuilder()
                    for i in f:
                        builder.add(
                            types.InlineKeyboardButton(
                        text=f"🔐 Дверь {count}", callback_data="lock_doors")
                        )
                        # msg += f"\n<b>📹 Камера {count} (<a href=\"DEUSecurity.com/cams/{i[0]}\"><u>{i[0]}</u></a>)</b>"
                        count += 1

                    await query.message.answer(msg, parse_mode="HTML", reply_markup=builder.as_markup())
                except:
                    pass
            elif(callback_data[1] == "Other devices"):
                # try:
                    count = 1
                    #getting from database
                    cur.execute("""SELECT * FROM W WHERE ownerID = ?""", (query.from_user.id,))
                    W = cur.fetchall()
                    cur.execute("""SELECT * FROM V WHERE ownerID = ?""", (query.from_user.id,))
                    V = cur.fetchall()
                    cur.execute("""SELECT * FROM T WHERE ownerID = ?""", (query.from_user.id,))
                    T = cur.fetchall()
                    list = [W,V,T]
                    if W == [] and V == [] and T == []:
                        await query.message.answer("Вы еще не добавили ни одного устройства")
                        return
                    msg = "Вот список всех устройств, которые привязаны к этому аккаунту:"
                    builder = InlineKeyboardBuilder()
                    for x in list:
                        print("if in list")
                        for i in x:
                            print('if in x')
                            if x == W:
                                builder.add(
                                    types.InlineKeyboardButton(
                                text=f"Окно {count}", callback_data="open_window")
                                )
                                count += 1
                            elif x == V:
                                builder.add(
                                    types.InlineKeyboardButton(
                                text=f"Пылесос {count}", callback_data="turn_vclean")
                                )
                                count += 1
                            elif x == T:
                                builder.add(
                                    types.InlineKeyboardButton(
                                text=f"Чайник {count}", callback_data="turn_tpot")
                                )
                                count += 1
                            
                        count = 1
                    builder.adjust(2,2)

                    await query.message.answer(msg, parse_mode="HTML", reply_markup=builder.as_markup())
                # except:
                #     pass
        elif("add" in callback_data.foo):
            await query.answer(f"You will be able to add device {callback_data.foo}")