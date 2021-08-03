import datetime

from bson import ObjectId
from flask import Flask, render_template, request
from pymongo import MongoClient

def create_app():
    app = Flask(__name__)
    client = MongoClient("mongodb+srv://gabrielandr:061284ga@mycroblobapp.qh3ja.mongodb.net/test")
    app.db = client.microblog
    entries = []


    @app.route("/", methods=["GET", "POST"])
    def home():
        if request.method == "POST":
            print([e for e in app.db.entries.find({})])
            date_format = "%b %d %H:%M:%S"
            date = datetime.datetime.today()
            formatted_date = date.strftime(date_format)
            entry_content = request.form.get("content")
            # entries.append((entry_content, formatted_date))
            app.db.entries.insert({"content": entry_content, "formatted_date": formatted_date})

        entries_with_date = [
            (
                entry["_id"],
                entry["content"],
                entry["formatted_date"]
            )
            for entry in app.db.entries.find({})
        ]
        return render_template("home.html", entries=entries_with_date)

    @app.route("/delete/<String:id>", methods=["DELETE"])
    def home(id):
        if request.method == "POST":
            app.db.entries.delete_one({"_id": ObjectId(id)})

        entries_with_date = [
            (
                entry["content"],
                entry["formatted_date"]
            )
            for entry in app.db.entries.find({})
        ]
        return render_template("home.html", entries=entries_with_date)
    return app