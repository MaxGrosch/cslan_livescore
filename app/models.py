from app import db


class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp_start = db.Column(db.Integer)
    timestamp_update = db.Column(db.Integer)
    map_name = db.Column(db.String(64), index=True)
    steam_id = db.Column(db.Integer, index=True)
    round_wins = db.Column(db.Integer)
    round_losses = db.Column(db.Integer)
    kills = db.Column(db.Integer)
    assists = db.Column(db.Integer)
    deaths = db.Column(db.Integer)
    mvps = db.Column(db.Integer)

    def __repr__(self):
        return f"<Match {self.id} - {self.map_name}: Stats for steam ID {self.steam_id}"
