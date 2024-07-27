from flask import Flask, request, jsonify
import sqlite3
import yaml
import os
from database2 import connection, createTable, insert, update, delete, select

app = Flask(__name__)

def openConfig(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)

config = openConfig(r"C:\Users\u47455\PycharmProjects\pythonProjectUserList\config3.yaml")

def getDb(sys_choice):
    list_conf = config[sys_choice]
    db_path = list_conf["file_path"]

    if not os.path.exists(db_path):
        c = connection(db_path)
        data_template = list_conf["data"]
        table_name = sys_choice

        columns = ", ".join([f"{field} TEXT" for field in data_template[0].keys()])
        createTable(c, table_name, columns)
        defaultListInit(c, table_name, data_template)
    else:
        c = connection(db_path)
    return c

def defaultListInit(c, table_name, data_template):
    if table_name == "user":
        user = ("KeremEnunlu", "kte@calik.com", "21")
        insert(c, f"INSERT INTO {table_name} (username, email, age) VALUES (?,?,?)", user)
    else:
        item = ("0", "Orange", "23TL")
        insert(c, f"INSERT INTO {table_name} (id, name, price) VALUES (?,?,?)", item)

@app.route("/add/<choice>", methods=["POST"])
def add(choice):
    if choice not in config:
        return jsonify({"Error": "Invalid choice."}), 400

    data_template = config[choice]["data"]
    table_name = choice
    c = getDb(choice)

    kwargs = request.json
    query = f"INSERT INTO {table_name} ({", ".join(kwargs.keys())}) VALUES ({", ".join("?" for _ in kwargs)})"
    params = tuple(kwargs.values())
    insert(c, query, params)

    return jsonify({"Message": "Entry added."})

@app.route("/update/<choice>", methods=["POST"])
def Update(choice):
    if choice not in config:
        return jsonify({"Error": "Invalid choice."}), 400

    data_template = config[choice]["data"]
    table_name = choice
    key = list(data_template[0].keys())[0]
    c = getDb(choice)

    kwargs = request.json
    value = kwargs.pop(key) # bu bize direk definitive (primary) key'i döndürerek kwargs'da sadece diğer keyleri bırakıyor, işlem kolaylığı sağlıyor.
    query = f"UPDATE {table_name} SET {", ".join([f'{k} = ?' for k in kwargs])} WHERE {key} = ?"
    params = (*kwargs.values(), value) # * işareti tuple dönüşümü için kullanılır. Burada tuple yapıp, value ile birleştirdik.
    updatedRows = update(c, query, params)

    if updatedRows == 0:
        kwargs[key] = value
        query = f"INSERT INTO {table_name} ({", ".join(kwargs.keys())}) VALUES ({", ".join("?" for _ in kwargs)})"
        params = tuple(kwargs.values())
        insert(c, query, params)
        return jsonify({"Warning": "Not found, update added as new entry."})
    else:
        return jsonify({"Message": "Entry updated."})

@app.route("/delete/<choice>", methods=["POST"])
def deletion(choice):
    if choice not in config:
        return jsonify({"Error": "Invalid choice."}), 400

    data_template = config[choice]["data"]
    table_name = choice
    c = getDb(choice)
    key = list(data_template[0].keys())[0]
    value = request.json[key] # sadece key yeterli

    query = f"DELETE FROM {table_name} WHERE {key} = ?" # Sadece key'in belirli bir değer olduğu zaman sil.
    deletedRows = delete(c, query, (value,))

    if deletedRows == 0:
        return jsonify({"Error": "Not found."})
    else:
        return jsonify({"Message": "Entry deleted."})

@app.route("/display/<choice>", methods=["GET"])
def display(choice):
    if choice not in config:
        return jsonify({"Error": "Invalid choice."}), 400

    table_name = choice
    c = getDb(choice)
    rows = select(c, f"SELECT * FROM {table_name}")
    return jsonify(rows)

if __name__ == "__main__":
    app.run(debug=True)