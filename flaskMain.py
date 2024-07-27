from flask import Flask, request, jsonify
import yaml
from database import connection, get_db, insert, update, delete, select

app = Flask(__name__)

def openConfig(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)

config = openConfig(r"C:\Users\u47455\PycharmProjects\pythonProjectUserList\config2.yaml")


@app.route("/add/<choice>", methods=["POST"])
def add(choice):
    if choice not in config:
        return jsonify({"Error": "Invalid choice."}), 400

    data_template = config[choice]["data"]
    queries = config[choice]["queries"]
    conn = get_db(config, choice)

    kwargs = request.json
    insert_query = queries["insert"]
    insert_params = tuple(kwargs[field] for field in data_template[0].keys())
    insert(conn, insert_query, insert_params)

    return jsonify({"Message": "Entry added."})


@app.route("/update/<choice>", methods=["POST"])
def update_entry(choice):
    if choice not in config:
        return jsonify({"Error": "Invalid choice."}), 400

    data_template = config[choice]["data"]
    queries = config[choice]["queries"]
    conn = get_db(config, choice)
    key = list(data_template[0].keys())[0]

    kwargs = request.json
    value = kwargs.pop(key)

    new_info = ", ".join([f"{k} = ?" for k in kwargs.keys()])
    update_query = f"UPDATE {choice} SET {new_info} WHERE {key} = ?"

    update_params = (*kwargs.values(), value)

    updatedRows = update(conn, update_query, update_params)

    if updatedRows == 0:
        kwargs[key] = value
        insert_query = queries["insert"]
        insert_params = tuple(kwargs[field] for field in data_template[0].keys())
        insert(conn, insert_query, insert_params)
        return jsonify({"Warning": "Not found, update added as new entry."})
    else:
        return jsonify({"Message": "Entry updated."})


@app.route("/delete/<choice>", methods=["POST"])
def delete_entry(choice):
    if choice not in config:
        return jsonify({"Error": "Invalid choice."}), 400

    data_template = config[choice]["data"]
    queries = config[choice]["queries"]
    conn = get_db(config, choice)
    key = list(data_template[0].keys())[0]
    value = request.json[key]

    delete_query = queries["delete"]
    delete_params = (value,)
    deletedRows = delete(conn, delete_query, delete_params)

    if deletedRows == 0:
        return jsonify({"Error": "Not found."})
    else:
        return jsonify({"Message": "Entry deleted."})


@app.route("/display/<choice>", methods=["GET"])
def display(choice):
    if choice not in config:
        return jsonify({"Error": "Invalid choice."}), 400

    queries = config[choice]["queries"]
    conn = get_db(config, choice)
    select_query = queries["select"]
    rows = select(conn, select_query)
    return jsonify(rows)


if __name__ == "__main__":
    app.run(debug=True)
