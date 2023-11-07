from app import app, db
from app.models import Match


def process_input_data(data: dict):
    features = extract_features(data)
    if is_competitive(features):
        match = get_match(features)
        if is_consistent_steamid(features):
            update_match(match, features)


def extract_features(data: dict) -> dict:
    provider = data.get("provider", {})
    map_data = data.get("map", {})
    previously = data.get("previously", {})
    player = data.get("player", {})
    match_stats = player.get("match_stats", {})

    return {
        "timestamp": provider.get("timestamp", 0),
        "provider_steamid": provider.get("steamid", "0"),
        "player_steamid": player.get("steamid", "0"),
        "player_name": player.get("name", ""),
        
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


def is_competitive(feat: dict) -> bool:
    return feat["map_mode"] == "competitive"


def is_consistent_steamid(feat: dict) -> bool:
    return feat["provider_steamid"] == feat["player_steamid"]


def get_match(feat: dict) -> Match:
    print("GET MATCH")
    match = get_latest_match(feat)
    if match is None:
        match = create_new_match(feat)
    elif is_inconsistent_latest_match(match, feat):
        match = create_new_match(feat)
    return match


def is_inconsistent_latest_match(match: Match, feat: dict) -> bool:
    return (
        ((feat["timestamp"] - match.timestamp_start) > 7200)  # two hours later
        or (feat["map_name"] != match.map_name)  # other map
    )


def create_new_match(feat: dict) -> Match:
    print("NEW MATCH")
    map_id = get_map_id(feat)
    match = Match(
        timestamp_start=feat["timestamp"],
        timestamp_update=feat["timestamp"],
        map_id=map_id,
        map_name=feat["map_name"],
        map_phase=feat["map_phase"],
        steamid=feat["provider_steamid"],
        player_name=feat["player_name"],
        round_wins=-1,
        round_losses=-1,
        kills=-1,
        assists=-1,
        deaths=-1,
        mvps=-1
    )
    db.session.add(match)
    return match


def get_map_id(feat: dict) -> int:
    map_id = 0
    match = Match.query.order_by(Match.map_id.desc()).first()
    if match is not None:
        time_diff = feat["timestamp"] - match.timestamp_start
        if time_diff >= 5 and time_diff <= 30 and (feat["map_name"] == match.map_name):
            map_id = match.map_id
        else:
            map_id = match.map_id + 1
    return map_id


def get_latest_match(feat: dict) -> Match:
    print("LATEST MATCH")
    match = Match.query.filter_by(steamid=feat["provider_steamid"]).order_by(Match.id.desc()).first()
    return match


def update_match(match: Match, feat: dict):
    match.timestamp_update = feat["timestamp"]
    match.map_phase = feat["map_phase"]
    match.round_wins = feat["map_ct_wins"] + feat["map_t_wins"]
    match.round_losses = feat["map_rounds"] - feat["map_ct_wins"] - feat["map_t_wins"]
    match.kills = feat["kills"]
    match.assists = feat["assists"]
    match.deaths = feat["deaths"]
    match.mvps = feat["mvps"]
    db.session.commit()
