from flask import render_template, request, make_response
from app import app
from app import database_operations as dataops


@app.route('/')
@app.route('/index')
def index():
    stats = [{"steam_id": "Kandidat", "games": 1, "wins": 1, "losses": 0, "rounds": 22, "kills": 22, "assists": 10, "deaths": 18, "dmg_done": 2000, "mvp": 5}]
    return render_template("index.html", title="CS2 LAN", stats=stats)


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
        dataops.update_database(data)
    return make_response("Success", 200)
