'''username and password to be stored in database. Explain the method to store the username and password in database'''
import sqlite3

def connect():
    conn=sqlite3.connect("Auth.db")
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS auth (id INTEGER PRIMARY KEY, user text, password text)")
    conn.commit()
    conn.close()


def checkUser(name):
    conn = sqlite3.connect("Auth.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM auth WHERE user=?",(name,))
    rows = cur.fetchall()
    conn.close()
    return rows




