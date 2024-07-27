import yaml
import sqlite3
from database2 import connection, createTable, insert, update, select, delete

def openConfig(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def defaultListInit(c, table_name, data_template):
    if "username" in data_template[0]:
        user = ("KeremEnunlu", "kte@calik@gmail.com", "21")
        insert(c, f"INSERT INTO {table_name} (username, email, age) VALUES (?,?,?)", user)
    else:
        item = ("0", "Orange", "23TL")
        insert(c, f"INSERT INTO {table_name} (id, name, price) VALUES (?,?,?)", item)

def readFromDatabase(c, table_name, data_template):
    rows = select(c, f"SELECT * FROM {table_name}")
    if not rows:
        defaultListInit(c, table_name, data_template)
        return readFromDatabase(c, table_name, data_template)
    else:
        return rows

def main():
    config = openConfig(r"C:\Users\u47455\PycharmProjects\pythonProjectUserList\config2.yaml")

    choice = input("Which app would you like to use? (user/grocery)?")
    if choice not in config:
        print("App not found, invalid app.")
        return

    list_conf = config[choice]
    path_to_db = list_conf["file_path"]
    data_template = list_conf["data"]
    table_name = choice
    key = list(data_template[0].keys())[0]

    c = connection(path_to_db)
    columns = ", ".join([f"{field} TEXT" for field in data_template[0].keys()])
    createTable(c, table_name, columns)

    while True:
        print(f"\n{choice.upper()} MANAGEMENT SYSTEM")
        print("1. Display List")
        print("2. Add Entry")
        print("3. Update Entry")
        print("4. Delete Entry")
        print("5. Exit")

        inp = input("\nEnter your choice: ")

        if inp == "1":
            rows = readFromDatabase(c, table_name, data_template)
            for row in rows:
                print(row)

        elif inp == "2":
            kwargs = {field: input(f"Enter {field}: ") for field in data_template[0]}
            query = f"INSERT INTO {table_name} ({', '.join(kwargs.keys())}) VALUES ({', '.join('?' for _ in kwargs)})"
            params = tuple(kwargs.values())
            insert(c, query, params)
            print("Entry added.")

        elif inp == "3":
            value = input(f"Enter {key} to update: ")
            kwargs = {field: input(f"Enter new {field}: ") for field in data_template[0] if field != key}
            query = f"UPDATE {table_name} SET {', '.join([f'{k} = ?' for k in kwargs])} WHERE {key} = ?"
            params = tuple(kwargs.values()) + (value,) # yeni girilen ve değişen değerler => kwargs.values() + username, yani (value,). bunların birleşimi yeni veriyi oluşturuyor.
            updatedRows = update(c, query, params)

            if updatedRows == 0:
                print("Not found, adding the entry as a new one.")
                kwargs[key] = value
                insert_query = f"INSERT INTO {table_name} ({', '.join(kwargs.keys())}) VALUES ({', '.join('?' for _ in kwargs)})"
                insert_params = tuple(kwargs.values())
                insert(c, insert_query, insert_params)
            else:
                print("Entry updated.")

        elif inp == "4":
            value = input(f"Enter {key} to delete: ")
            query = f"DELETE FROM {table_name} WHERE {key} = ?"
            deletedRows = delete(c, query, (value,))

            if deletedRows == 0:
                print("Entry not found.")
            else:
                print("Entry deleted.")

        elif inp == "5":
            print("Terminating program...")
            break

        else:
            print("Invalid input.")

    c.close()

if __name__ == "__main__":
    main()
