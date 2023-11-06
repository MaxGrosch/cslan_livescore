from app import db
from app.models import Match

## TODO:
# - IMPORTANT: match.id NOT NULL constraint failed? Autoincrement?
# - use max() in update logic?
# - sanity checks when retrieving match

def process_input_data(data: dict):
    features = extract_features(data)
    con = continue_processing(features)
    print(f"{con} - {type(con)}")
    if continue_processing(features):
        match = get_match(features)
        update_match(match, features)


def extract_features(data: dict) -> dict:
    provider = data.get("provider", {})
    map_data = data.get("map", {})
    previously = data.get("previously", {})
    player = data.get("player", {})
    match_stats = player.get("match_stats", {})

    return {
        "steam_id": provider.get("steamid", 0),
        "timestamp": provider.get("timestamp", 0),
        
        "map_name": map_data.get("name", "unavailable"),
        "map_mode": map_data.get("mode", "unavailable"),  # search for competitive
        "map_phase": map_data.get("phase", "unavailable"),  # search for live
        "map_previous_phase": previously.get("map", {}).get("phase", "unavailable"),

        "map_rounds": map_data.get("round", -1),
        "map_ct_wins": map_data.get("team_ct", {}).get("score", -1),
        "map_t_wins": map_data.get("team_t", {}).get("score", -1),

        "kills": match_stats.get("kills", -1),
        "assists": match_stats.get("assists", -1),
        "deaths": match_stats.get("deaths", -1),
        "mvps": match_stats.get("mvps", -1)
    }


def continue_processing(feat: dict) -> bool:
    return (feat["map_mode"] == "competitive"
            and feat["map_phase"] != "warmup")


def get_match(feat: dict) -> Match:
    if match_start_conditions(feat):
        match = create_new_match(feat)
    else:
        match = get_latest_match(feat)
    return match


def match_start_conditions(feat: dict) -> bool:
    return (feat["map_phase"] == "live" 
            and feat["map_previous_phase"] == "warmup"
            and feat["map_rounds"] == 0)


def create_new_match(feat: dict) -> Match:
    match = Match(
        timestamp_start=feat["timestamp"],
        timestamp_update=feat["timestamp"],
        map_name=feat["map_name"],
        steam_id=feat["steam_id"],
        round_wins=-1,
        round_losses=-1,
        kills=-1,
        assists=-1,
        deaths=-1,
        mvps=-1
    )
    return match


def get_latest_match(feat: dict) -> Match:
    match = Match.query.filter_by(steam_id=feat["steam_id"]).order_by(Match.id.desc()).first()
    return match


def update_match(match: Match, feat: dict):
    match.timestamp_update = feat["timestamp"]
    match.round_wins = feat["map_ct_wins"] + feat["map_t_wins"]
    match.round_losses = feat["map_rounds"] - feat["map_ct_wins"] - feat["map_t_wins"]
    match.kills = feat["kills"]
    match.assists = feat["assists"]
    match.deaths = feat["deaths"]
    match.mvps = feat["mvps"]
    db.session.add(match)
    db.session.commit()
