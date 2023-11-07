from app import db


class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    steamid = db.Column(db.String(64), index=True)
    player_name = db.Column(db.String(128))
    map_id = db.Column(db.Integer, index=True)
    map_name = db.Column(db.String(64), index=True)
    map_phase = db.Column(db.String(64))
    timestamp_start = db.Column(db.Integer)
    timestamp_update = db.Column(db.Integer)
    round_wins = db.Column(db.Integer)
    round_losses = db.Column(db.Integer)
    kills = db.Column(db.Integer)
    assists = db.Column(db.Integer)
    deaths = db.Column(db.Integer)
    mvps = db.Column(db.Integer)

    def __repr__(self):
        return f"<Match {self.id} - {self.map_name} - {self.map_id}>"


# class Player(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     steamid = db.Column(db.String(64), index=True, unique=True)
#     name = db.Column(db.String(128))

#     def __repr__(self):
#         return f"<Player {self.id} - {self.player_name}>"