import sqlite3

def connection(path):
    return sqlite3.connect(path)

def createTable(c, table_name, cols):
    c.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({cols})")
    c.commit()

def insert(c, query, params):
    c.execute(query, params)
    c.commit()

def update(c, query, params):
    cursor = c.execute(query, params)
    c.commit()
    return cursor.rowcount

def select(c, query, params=()):
    cursor = c.execute(query, params)
    return cursor.fetchall()

def delete(c, query, params):
    cursor = c.execute(query, params)
    c.commit()
    return cursor.rowcount
