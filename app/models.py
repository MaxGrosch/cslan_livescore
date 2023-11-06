from app import db


# class LANStats(db.Model):
#     steam_id = db.Column(db.Integer, primary_key=True)
#     games = db.Column(db.Integer)
#     wins = db.Column(db.Integer)
#     losses = db.Column(db.Integer)
#     rounds = db.Column(db.Integer)
#     kills = db.Column(db.Integer)
#     assists = db.Column(db.Integer)
#     deaths = db.Column(db.Integer)
#     dmg_done = db.Column(db.Integer)
#     mvp = db.Column(db.Integer)

#     def __repr__(self):
#         return f"<LANStats for {self.steam_id}>"


class Match(db.Model):
    match_id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.Integer)
    steam_id = db.Column(db.Integer)
    round_wins = db.Column(db.Integer)
    round_losses = db.Column(db.Integer)
    kills = db.Column(db.Integer)
    assists = db.Column(db.Integer)
    deaths = db.Column(db.Integer)
    mvp = db.Column(db.Integer)

    def __repr__(self):
        return f"<Match {self.match_id}: Stats for steam ID {self.steam_id}"

