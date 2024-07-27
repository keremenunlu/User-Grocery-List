import sqlite3
import yaml

def openConfig(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def createTable(c, table_name, data_template):
    columns = ", ".join([f"{field} TEXT" for field in data_template[0].keys()])
    c.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})")
    c.commit()

def defaultListInit(c, table_name, data_template):
    if "username" in data_template[0]:
        user = ("KeremEnunlu", "kte@calik@gmail.com", "21")
        c.execute(f"INSERT INTO {table_name} (username, email, age) VALUES (?,?,?)", user)
    else:
        item = ("0", "Orange", "23TL")
        c.execute(f"INSERT INTO {table_name} (id, name, price) VALUES (?,?,?)", item)
    c.commit()

def readFromDataBase(c, table_name, data_template):
    cursor = c.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    if len(rows) == 0:
        defaultListInit(c, table_name, data_template)
        return readFromDataBase(c, table_name, data_template)
    else:
        return rows

def add(c, table_name, **kwargs):
    columns = ", ".join(kwargs.keys())
    locations = ", ".join("?" for i in kwargs) # kwargs argümanı sayısı kadar yer ayırma
    values = tuple(kwargs.values()) # eklenecek değerleri toplama
    c.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({locations})", values)
    c.commit()

def update(c, table_name, key, **kwargs):
    count = 0

    theSet = ", ".join([f"{k} = ?" for k in kwargs]) # column eşleştirmeleri
    values = tuple(kwargs.values())
    cursor = c.execute(f"UPDATE {table_name} SET {theSet} WHERE {key} = ?", (*values, kwargs[key])) # keylerin eşleşmesi durumunda diğer özelliklere value'ları yerleştir

    if cursor.rowcount == 0:
        print("Not found, adding the entry as a new one.")
        add(c, table_name, **kwargs)
    c.commit()

def delete(c, table_name, key, value):
    cursor = c.execute(f"DELETE FROM {table_name} WHERE {key} = ?", (value,)) # sondaki , tuple yapmak için, güvenli bir şekilde sql'e bu şekilde işleniyor. {key} = {value} olarak yazmak doğru ama injection riski var
    if cursor.rowcount == 0:
        print("Not found.")
    c.commit()

def displayList(c, table_name):
    cursor = c.execute(f"SELECT * FROM {table_name}")
    for rows in cursor.fetchall():
        print(rows)

def main():
    config = openConfig(r"C:\Users\u47455\PycharmProjects\pythonProjectUserList\config2.yaml")

    choice = input("Which app would you like to use? (user/grocery)?")
    if choice not in config:
        print("App not found, invalid app.")
        return
    else:
        list_conf = config[choice]
        path_to_db = list_conf["file_path"]
        data_template = list_conf["data"]
        table_name = choice
        key = list(data_template[0].keys())[0] # birden çok entry var, yani bu bir list of dictionaries. o yüzden key = list(data_template.keys())[0] kullanırsak bize ilk dictionary verilir, ancak bize onun o dict. içindeki ilk (0.) key gerek.

        c = sqlite3.connect(path_to_db)
        createTable(c, table_name, data_template)

        readFromDataBase(c, table_name, data_template) # db boşsa kendimiz değer atayarak başlattık

        while True:
            print(f"\n{choice.upper()} MANAGEMENT SYSTEM")
            print("1. Display List")
            print("2. Add Entry")
            print("3. Update Entry")
            print("4. Delete Entry")
            print("5. Exit")

            inp = input("\nEnter your choice: ")

            if inp == "1":
                displayList(c, table_name)
            elif inp == "2":
                kwargs = {field: input(f"Enter {field}: ") for field in data_template[0]}
                add(c, table_name, **kwargs)
            elif inp == "3":
                value = input(f"Enter {key} to update: ")
                kwargs = {field: input(f"Enter new {field}: ") for field in data_template[0] if field != key}
                kwargs[key] = value
                update(c, table_name, key, **kwargs)
            elif inp == "4":
                value = input(f"Enter {key} to delete: ")
                delete(c, table_name, key, value)
            elif inp == "5":
                print("Terminating program...")
                break
            else:
                print("Invalid input.")

        c.close()

if __name__ == "__main__":
    main()
