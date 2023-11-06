def update_database(data: dict):
    timestamp = data.get("provider").get("timestamp")
    steam_id = data.get("provider").get("steamid")
    map_mode = data.get("map").get("mode")
    map_phase = data.get("map").get("phase")

    if map_mode is "competitive" and map_phase is "live" and map_round:
        print("")

    print(data)


    steam_id = db.Column(db.Integer, primary_key=True)
    games = db.Column(db.Integer)
    wins = db.Column(db.Integer)
    losses = db.Column(db.Integer)
    rounds = db.Column(db.Integer)
    kills = db.Column(db.Integer)
    assists = db.Column(db.Integer)
    deaths = db.Column(db.Integer)
    dmg_done = db.Column(db.Integer)
    mvp = db.Column(db.Integer)