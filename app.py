#  Copyright © 2023 te4gh0st (Vitaliy Timtsurak). All rights reserved.
#  Licensed under the Apache License, Version 2.0

from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo
from datetime import datetime

import webbrowser


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://mongodb:27017/myDatabase"
mongo = PyMongo(app)
Bootstrap(app)
webbrowser.open('http://localhost:8080/', new=1)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        action = request.form.get('action')
        collection = mongo.db.myCollection

        if action == 'insert_one':
            data = request.form.to_dict(flat=False)
            data.pop('action', None)
            document = {data[f'field_name_{i}'][0]: data[f'field_value_{i}'][0] for i in range(1, (len(data) // 2) + 1)}
            collection.insert_one(document)

        if action == 'find':
            query_field = request.form['query_field']
            query_value = request.form['query_value']
            query = {query_field: query_value} if query_value else {query_field: {"$exists": True}}
            results = list(collection.find(query))
            return render_template('index.html', results=results, year=datetime.now().year)

        if action == 'find_one':
            query_field = request.form['query_field_one']
            query_value = request.form['query_value_one']
            query = {query_field: query_value} if query_value else {query_field: {"$exists": True}}
            results = collection.find_one(query)
            return render_template('index.html', results=results, year=datetime.now().year)

        if action == 'update':
            query_field = request.form['query_field_update']
            query_value = request.form['query_value_update']
            update_key = request.form['update_key']
            update_value = request.form['update_value']
            query = {query_field: query_value} if query_value else {query_field: {"$exists": True}}
            collection.update_many(query, {"$set": {update_key: update_value}})

        if action == 'delete':
            query_field = request.form['query_field_delete']
            query_value = request.form['query_value_delete']
            query = {query_field: query_value} if query_value else {query_field: {"$exists": True}}
            collection.delete_many(query)

        return redirect(url_for('index'))

    return render_template('index.html', year=datetime.now().year)


if __name__ == '__main__':
    app.run(debug=True)
