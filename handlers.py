from aiogram import types, F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton,  KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from db import cur, con
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
router = Router()

database = ""



class MyCallback(CallbackData, prefix="my"):
    foo: str
    bar: int

class AddDevice(StatesGroup):
    waiting_for_device_id = State()
    waiting_for_device_type = State()

class StatesMachineDevice():
    @router.message(Command("cancel"))
    async def cancel_state_editing(message: Message, state: FSMContext):
        await state.clear()
        await message.answer("Добавление устройства отменено", reply_markup=s_builder.as_markup(resize_keyboard=True))
    async def device_start(message: types.Message, state: FSMContext):
        
        global avalible_device_types
        avalible_device_types = ["C","D","L","T","L","V","W"]
        keyboard = ReplyKeyboardBuilder()
        for name in avalible_device_types:
            keyboard.add(KeyboardButton(text=f"{name}"))
        await message.answer("""
Камера - C
Свет - L
Дверь - D
Окно - W
Чайник - T
Пылесос - V 
Выберите тип девайса:""", reply_markup=keyboard.as_markup(resize_keyboard=True))
        await state.set_state(AddDevice.waiting_for_device_type)




@router.message(AddDevice.waiting_for_device_type)
async def food_chosen(message: Message, state: FSMContext):
    if(message.text not in avalible_device_types):
        
        await message.answer("Такого типа не существует")
        await StatesMachineDevice.device_start(message=message, state=state)
        return
    await state.update_data(chosen_type=message.text)
    await message.answer(
        text="Теперь напишите уникальный ID с боковой стороны устройства:",
    )
    await state.set_state(AddDevice.waiting_for_device_id)


@router.message(AddDevice.waiting_for_device_id)
async def food_size_chosen(message: Message, state: FSMContext):
    
    user_data = await state.get_data()
    messageD = await message.answer("Проверяю наличие кода в базе данных")
    dtype = user_data["chosen_type"]
    cur.execute(f"SELECT * FROM {dtype} WHERE deviceID = ?", (message.text,))
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
        cur.execute(f"""INSERT INTO {dtype}(deviceID, ownerID) VALUES(?,?)""", (message.text, message.from_user.id))
        con.commit()
        await messageD.edit_text("Устройство успешно добавлено в базу данных")
    except:
        await messageD.edit_text("Непредвиденная ошибка, обратитесь в тех поддержку")
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text="➕ Добавить девайс"),
        types.KeyboardButton(text="🔧 Управление девайсами"),
        types.KeyboardButton(text="⚙️ Настройки")
    )
    await message.answer(
        text=f"Вы добавили {dtype} устройсво с ID {message.text}.\n",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )
    # Сброс состояния и сохранённых данных у пользователя
    await state.clear()


class globalHandlers():
    
    @router.message(Command("start"))
    async def start_handler(msg: Message):
        try:
            cur.execute("""INSERT INTO users(id, username) VALUES(?,?)""", (msg.from_user.id, msg.from_user.username))
            con.commit()
        except:
            pass
        global s_builder
        s_builder = ReplyKeyboardBuilder()
        s_builder.row(
        types.KeyboardButton(text="➕ Добавить девайс"),
        types.KeyboardButton(text="🔧 Управление девайсами"),
        types.KeyboardButton(text="⚙️ Настройки")
        )
        await msg.answer('''
Здравствуйте, вас приветствует компания <b>DEU Security</b>
Снизу появилось меню управления ботом, если вы используете его впервые, нажмите на "Добавить девайс"
''', parse_mode="HTML",reply_markup=s_builder.as_markup(resize_keyboard=True))
        
    @router.message(Command("support"))
    async def getSupportContact(message: Message):
            await message.answer("<b>Аккаунт тех. поддержки: @Maykya\n\nУчтите, что вам <u>запрещено спамить</u>, в таком случае вы никогда не получите ответа на свой вопрос</b>")

    @router.message(Command("get_website"))
    async def send_websitelink(message: Message):

        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(text="Тык!", url="http://project7992405.tilda.ws/"))
        await message.answer("<b>Эта кнопка перенаправит вас на наш веб-сайт</b>", parse_mode="HTML", reply_markup=builder.as_markup())
    
    @router.message()
    async def check_message(message: Message, state: FSMContext):
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
        elif("Добавить девайс" in message.text):
            print("html")
            await StatesMachineDevice.device_start(message=message, state=state)

        elif("Настройки" in message.text):
            builder = InlineKeyboardBuilder()
            builder.add(InlineKeyboardButton(text=" 📄 Сценарии", callback_data="Scenes"))
            builder.add(InlineKeyboardButton(text=" 🙋 Тех. Поддержка", callback_data=MyCallback(foo="Support", bar=1).pack()))
            builder.add(InlineKeyboardButton(text=" 🔒 Настройки умной безопасности", callback_data=MyCallback(foo="SecuritySettings", bar=1).pack()))
            builder.adjust(2,2)
            await message.answer("""Вы зашли в настройки DEU Security
Снизу вы можете увидеть меню, для управления чат-ботом                                 
""",parse_mode="HTML",reply_markup=builder.as_markup())
    @router.message(AddDevice.waiting_for_device_id)
    async def dtype(message: Message, state: FSMContext):
        StatesMachineDevice.device_chosen(message=message, state=state)

   
class userHandlers():
    pass


class adminHandlers():
    pass


class callbacks():
    @router.callback_query(MyCallback.filter())
    async def my_callback_foo(query: CallbackQuery, callback_data: MyCallback):
        print(f"Hello {callback_data.foo}")
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
                        for i in x:
                            if x == W:
                                builder.add(
                                    types.InlineKeyboardButton(
                                text=f"Окно {count}", callback_data=MyCallback(foo="mdevice_window", bar=1).pack())
                                )
                                count += 1
                            elif x == V:
                                builder.add(
                                    types.InlineKeyboardButton(
                                text=f"Пылесос {count}", callback_data=MyCallback(foo="mdevice_vcleaner", bar=1).pack())
                                )
                                count += 1
                            elif x == T:
                                builder.add(
                                    types.InlineKeyboardButton(
                                text=f"Чайник {count}", callback_data=MyCallback(foo="mdevice_teapot", bar=1).pack())
                                )
                                count += 1
                            
                        count = 1
                    builder.adjust(2,2)

                    await query.message.answer(msg, parse_mode="HTML", reply_markup=builder.as_markup())
                # except:
                #     pass
        elif("add" in callback_data.foo):
            await query.answer(f"You will be able to add device {callback_data.foo}")
        elif("mdevice" in callback_data.foo):
            # if(callback_data.foo.split("_")[1] == "window"):
            device = callback_data.foo.split("_")[1]
            await query.message.answer(f"You will be able to manage {device}s soon...")
        elif(callback_data.foo == "Support"):
            await query.message.answer("<b>Аккаунт тех. поддержки: <u>@Maykya</u></b>", parse_mode="HTML")
        elif(callback_data.foo == "Scenes"):
            await query.message.answer("Soon...")
        elif(callback_data.foo == "SecuritySettings"):
            builder = InlineKeyboardBuilder()
            builder.add(InlineKeyboardButton(text="Вкл/Выкл автоматическую защиту", callback_data="pass"))
            builder.add(InlineKeyboardButton(text="Вкл/Выкл сканирование местности ИИ", callback_data="pass"))
            builder.add(InlineKeyboardButton(text="Вкл/Выкл уведомления о подозрительных вещах", callback_data="pass"))
            builder.adjust(1,1)
            await query.message.answer("<b>Меню настройки:</b>",parse_mode="HTML", reply_markup=builder.as_markup())
        
