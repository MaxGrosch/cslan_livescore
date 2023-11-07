from flask import render_template, request
from app import app, db
from app import database_operations as dataops
from app import data_preparation as dataprep
from app.models import Match

import pandas as pd


@app.route("/health_check", methods=["GET"])
def health_check():
    return "200 - Server up and running"


@app.route('/')
@app.route('/matches')
def matches():
    data = get_data("match")
    prepared = dataprep.prepare_matches(data)
    overview = dataprep.match_overview(prepared)
    return render_template("matches.html", overview=overview.to_html(), matches=prepared.to_html())


@app.route("/stats")
def stats():
    n_last = request.args.get("n_last", default=-1, type=int)
    data = get_data("match")
    filtered = dataprep.filter_last_matches(data, n_last)
    prepared = dataprep.prepare_stats(filtered)
    return render_template("stats.html", stats=prepared.to_html())


@app.route("/receive_gsi", methods=["GET", "POST"])
def receive_gsi():
    print("Received request!")
    data = None
    try:
        data = eval(request.data)
    except NameError:
        data = None
    if isinstance(data, dict):
        print(data)
        dataops.process_input_data(data)
    return "Successfully received data"


def get_data(table: str):
    with db.engine.connect() as connection:
        df = pd.read_sql(table, connection)
    return df
