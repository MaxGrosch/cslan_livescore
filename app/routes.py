from flask import render_template, request
from app import app
from app import database_operations as dataops
from app.models import Match


@app.route('/')
@app.route('/matches')
def matches():
    matches = Match.query.all()
    print(matches)
    return render_template("matches.html", matches=matches)


@app.route("/health_check", methods=["GET"])
def health_check():
    return "200 - Server up and running"


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
