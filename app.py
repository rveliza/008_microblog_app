from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv

import datetime, os

load_dotenv()

def create_app():

    app = Flask(__name__)
    mongo_pwd = ""
    client = MongoClient(os.getenv("MONGODB_URI"))    
    app.db = client.microblog

    @app.route("/", methods=["GET", "POST"])
    def home():
        # db_entries = [e for e in app.db.entries.find({})]
        if request.method == "POST":
            entry_content = request.form.get('content')
            formatted_date = datetime.datetime.today().strftime('%Y-%m-%d')
            app.db.entries.insert_one({
                'content': entry_content,
                'date': formatted_date
            })

        entries_with_date = [
            (
                entry['content'],
                entry['date'],
                datetime.datetime.today().strftime('%b %d')
            )
            # for entry in db_entries
            for entry in app.db.entries.find({})
        ]
        return render_template("home.html", entries=entries_with_date)
    return app