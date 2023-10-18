import sqlite3



def main():
    global con, cur
    con = sqlite3.connect("Da.db")
    cur = con.cursor()
    command = ""
    while True:
        command = input("""
1. Просмотреть всю таблицу
2. Просмотреть конкретную запись в таблице
3. Добавить девайс(Прямое добавление через код)
4. Добавить в таблицу
Введите номер сценария:
""")
        if int(command) == 1:
            name = input("\nВведите название таблицы: ")
            cur.execute(f"SELECT * FROM {name}")
            print(cur.fetchall())
        elif int(command) == 2:
            name = input("\nВведите название таблицы: ")
            cur.execute(f"SELECT * FROM {name}")
            print(cur.fetchall())
        elif int(command) == 3:
            dtypes = {
                1: "Cameras",
                2: "Light",
                3: "Door",
                4: "Window",
                5: "TeaPot",
                6: "VCleaner",
            }
            deviceID = input("\nВведите название код устройства(6 символов): ")
            deviceType = dtypes[int(input("""
1. Камера
2. Свет
3. Дверь
4. Окно
5. Чайник
6. Пылесос
Введите тип девайса: """))]
            cur.execute(f"""SELECT * FROM allDevices WHERE deviceID = ?""", (deviceID,))
            if not cur.fetchall() == []:
                print("Девайс с таким ID уже есть в базе данных ")
                return
            cur.execute("""INSERT INTO allDevices(deviceID, deviceType) VALUES(?,?)""", (deviceID, deviceType))
            con.commit()
            cur.execute("""SELECT * FROM allDevices""")
            a = cur.fetchall()
            print(a)
            print(f"Девайс успешно добавлен {len(a)}")  
        elif int(command) == 4:
            name = input("\nВведите название таблицы: ")
            cur.execute(f"SELECT * FROM {name}")
            print(cur.fetchall())
            id = input("Введите ID девайса: ")
            uid = input("Введите ID владельца: ")
            cur.execute(f"""INSERT INTO {name}(deviceID, ownerID) VALUES(?,?)""", (id, uid))
            con.commit()


if __name__ == "__main__":
    main()