import sqlite3

con = sqlite3.connect("Da.db")
cur = con.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
            username VARCHAR(255),
            admin BOOLEAN DEFAULT FALSE
)""")

#Cameras
cur.execute("""CREATE TABLE IF NOT EXISTS C(
            deviceID VARCHAR(255) UNIQUE,
            ownerID INTEGER
)""")
#Lights
cur.execute("""CREATE TABLE IF NOT EXISTS L(
            deviceID VARCHAR(255) UNIQUE,
            ownerID INTEGER
)""")
#Doors
cur.execute("""CREATE TABLE IF NOT EXISTS D(
            deviceID VARCHAR(255) UNIQUE,
            ownerID INTEGER
)""")
#Windows
cur.execute("""CREATE TABLE IF NOT EXISTS W(
            deviceID VARCHAR(255) UNIQUE,
            ownerID INTEGER
)""")
#VCleaners
cur.execute("""CREATE TABLE IF NOT EXISTS V(
            deviceID VARCHAR(255) UNIQUE,
            ownerID INTEGER
)""")
#Teapots
cur.execute("""CREATE TABLE IF NOT EXISTS T(
            deviceID VARCHAR(255) UNIQUE,
            ownerID INTEGER
)""")
cur.execute("""CREATE TABLE IF NOT EXISTS allDevices(
            deviceID VARCHAR(255) UNIQUE,
            deviceType VARCHAR(255)
)""")