from flask import Flask, render_template, request, redirect, url_for
import uuid
import uuid
import os
import json
app = Flask(__name__)
DATA_FILE = "/data/todo_data.json" if "AMVERA" in os.environ else "todo_data.json"

def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
def save_data(data_list):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data_list, f, ensure_ascii=False, indent=2)

data = load_data()

@app.route("/")
def index():
    return render_template("index.html", todo_list = data, count = len(data))

@app.route("/change_status/<id>")
def change_status(id):
    for item in data:
        if item["id"] == id:
            item["status"] = not item["status"]
            
            
            
    save_data(data)
    return redirect(url_for("index"))



@app.route("/del/<id>")
def del_item(id):
    for item in data:
        if item["id"] == id:
            data.remove(item)
    save_data(data)
    return redirect(url_for("index"))



@app.route("/search", methods=["POST"])
def search_item():
    searching_word = request.form.get("search_item")
    search_list = []

    for item in data:
        if searching_word in item["text"]:
            search_list.append(item)

    return render_template("index.html", todo_list = search_list, count = len(data))



@app.route("/add_item", methods=["POST"])
def add_item():
    text = request.form.get("item")
    if not text:
        return redirect(url_for("index"))
    item = {
        "id": str(uuid.uuid4()),
        "text": text,
        "status": False
    }

    data.append(item)
    save_data(data)     

    print(data)
    return redirect(url_for("index"))





if __name__ == '__main__':
    app.run(port=8000)