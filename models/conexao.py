import sqlite3

def sqlite_connector():
    mydb = sqlite3.connect('espeto_madeira.db')
    return mydb