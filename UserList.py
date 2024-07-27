import json
import yaml

def openConfig(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)

def createDictList(data_template):
    data_list = []
    return data_list

def defaultListInit(data_template):
    data_list = createDictList(data_template)

    if "username" in data_template[0]: # eğer "username" data_template'in başında var ise, bu demektir ki biz bir userList kullanacağız.
        user = {
            "username": "KeremEnunlu",
            "email": "kte@calik.com",
            "age": "21"}

        data_list.append(user)

    else:
        item = {
            "id": "0",
            "name": "Orange",
            "price": "3TL"}

        data_list.append(item)

    return data_list

def writeToJson(path, data_list):
    with open(path, "w") as f:
        json.dump(data_list, f)

def readFromJson(path, data_template):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data_list = defaultListInit(data_template)
        writeToJson(path, data_list)
        return data_list

def add(data_list, path, **kwargs): # **kwargs = keyword arguments, gerektiği sayıda keylerin value'larını parametre olarak girmek için kullanılıyor.
    data_list.append(kwargs)
    writeToJson(path, data_list)

def update(data_list, path, key, **kwargs):
    count = 0

    for i in data_list:
        if i[key] == kwargs[key]: # i'deki key ve kwargs'daki key value'ları eşitse
            for Key, Value in kwargs.items():
                i[Key] = Value # kwargs value'sunu key değerine atama
            writeToJson(path, data_list)

            count = 1
            break

    if count == 0:
        print("Not found, adding the entry as a new one.")
        add(data_list, path, **kwargs)

def delete(data_list, path, key, value):
    count = 0

    for i in data_list:
        if i[key] == value:
            data_list.remove(i)
            writeToJson(path, data_list)

            count = 1
            break

    if count == 0:
        print("Not found.")

def displayList(data_list):
    for i in data_list:
        print(i)

def main():
    config = openConfig(r"C:\Users\u47455\PycharmProjects\pythonProjectUserList\config.yaml")

    choice = input("Which app would you like to use? (user/grocery)?")
    if choice not in config:
        print("Not found, invalid app.")
        return

    list_conf = config[choice]
    path = list_conf["file_path"]
    data_template = list_conf["data"]
    key = list(data_template[0].keys())[0] #ilk key'i özel belirtken olarak yerleştirdik.
    data_list = readFromJson(path, data_template)

    while True:
        print(f"\n{choice.upper()} MANAGEMENT SYSTEM")
        print("1. Display List")
        print("2. Add Entry")
        print("3. Update Entry")
        print("4. Delete Entry")
        print("5. Exit")

        inp = input("\nEnter your choice: ")

        if inp == "1":
            displayList(data_list)

        elif inp == "2":
            kwargs = {field: input(f"Enter {field}: ") for field in data_template[0]} # data_template[0] = data
            add(data_list, path, **kwargs)

        elif inp == "3":
            value = input(f"Enter {key} to update: ")
            kwargs = {field: input(f"Enter new {field}: ") for field in data_template[0] if field != key} # data_template[0] = data
            kwargs[key] = value
            update(data_list, path, key, **kwargs)

        elif inp == "4":
            value = input(f"Enter {key} to delete: ")
            delete(data_list, path, key, value)

        elif inp == "5":
            print("Terminating program...")
            break

        else:
            print("Invalid input.")

if __name__ == "__main__":
    main()
