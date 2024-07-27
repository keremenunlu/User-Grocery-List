import sqlite3
import os

def connection(path):
    return sqlite3.connect(path)

def create_table(conn, query):
    conn.execute(query)
    conn.commit()

def insert(conn, query, params):
    conn.execute(query, params)
    conn.commit()

def update(conn, query, params):
    cursor = conn.execute(query, params)
    conn.commit()
    return cursor.rowcount

def select(conn, query, params=()):
    cursor = conn.execute(query, params)
    return cursor.fetchall()

def delete(conn, query, params):
    cursor = conn.execute(query, params)
    conn.commit()
    return cursor.rowcount

def get_db(config, sys_choice):
    list_conf = config[sys_choice]
    db_path = list_conf["file_path"]

    if not os.path.exists(db_path):
        conn = connection(db_path)
        query = list_conf["queries"]["create_table"]
        create_table(conn, query)
        default_list_init(conn, sys_choice, config)
    else:
        conn = connection(db_path)
    return conn

def default_list_init(conn, table_name, config):
    if table_name == "user":
        user = ("KeremEnunlu", "kte@calik.com", "21")
        query = config["user"]["queries"]["insert"]
        insert(conn, query, user)
    else:
        item = ("0", "Orange", "23TL")
        query = config["grocery"]["queries"]["insert"]
        insert(conn, query, item)
