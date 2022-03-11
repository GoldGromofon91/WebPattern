import sqlite3
"""
Скрипт создания структуры БД
"""
con = sqlite3.connect('db.sqlite')
cur = con.cursor()
with open('create-skelet-db.sql', 'r') as f:
    text = f.read()
cur.executescript(text)
cur.close()
con.close()
