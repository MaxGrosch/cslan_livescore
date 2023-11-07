import numpy as np
import pandas as pd

def prepare_matches(data: pd.DataFrame) -> pd.DataFrame:
    grouper = data.groupby("map_id")

    timestamp = grouper["timestamp_start"].min()
    timestamp = pd.to_datetime(timestamp, unit="s")
    timestamp.name = "timestamp"

    map_name = grouper["map_name"].first()

    rounds = grouper[["round_wins", "round_losses"]].first()
    rounds["result"] = rounds.apply(determine_result, axis=1)

    number_lan_players = grouper.nunique()[["steamid"]]
    number_lan_players.columns = ["lan_players"]
    lan_players = grouper["player_name"].unique()
    lan_players.name = "player_names"

    response = pd.concat([timestamp, map_name, rounds, number_lan_players, lan_players], axis=1)
    response_cols = ["timestamp", "map_name", "result", "round_wins", "round_losses", "lan_players", "player_names"]
    return response[response_cols]


def determine_result(rounds):
    round_wins = rounds["round_wins"]
    round_losses = rounds["round_losses"]
    result = "unknown"
    if (round_wins >= 13 and round_losses < 12) or round_wins > 15:
        result = "win"
    elif (round_losses >= 13 and round_wins < 12) or round_losses > 15:
        result = "loss"
    elif round_wins == 15 and round_losses == 15:
        result = "tie"
    return result


def match_overview(matches: pd.DataFrame) -> pd.DataFrame:
    all_maps = matches.groupby("result").count()["map_name"]
    all_maps.name = "all_maps"
    all_maps = all_maps.to_frame().transpose()

    individual_maps = matches.groupby(["map_name", "result"]).count()["timestamp"]
    individual_maps.name = "count"
    individual_maps = individual_maps.reset_index()
    individual_maps = individual_maps.pivot(index="map_name", columns="result", values="count")

    overview = pd.concat([all_maps, individual_maps], axis=0).fillna(0)
    return overview


def prepare_stats(data: pd.DataFrame) -> pd.DataFrame:
    grouper = data.groupby("steamid")
    
    player_name = grouper["player_name"].last()

    maps_played = grouper.nunique()[["map_id"]]
    maps_played.columns = ["maps_played"]

    sum_cols = ["round_wins", "round_losses", "kills", "assists", "deaths", "mvps"]
    summed = grouper.sum()[sum_cols]
    summed["total_rounds"] = summed["round_wins"] + summed["round_losses"]
    summed["avg_kpr"] = summed["kills"] / summed["total_rounds"]
    summed["avg_apr"] = summed["assists"] / summed["total_rounds"]
    summed["avg_dpr"] = summed["deaths"] / summed["total_rounds"]
    
    response = pd.concat([player_name, maps_played, summed], axis=1)
    response_cols = ["player_name", "maps_played", "total_rounds", "kills", "assists", "deaths", "mvps", "avg_kpr", "avg_apr", "avg_dpr"]
    return response[response_cols]


def filter_last_matches(data: pd.DataFrame, n_last: int = 0):
    result = data
    if n_last >= 0:
        result = data.sort_values("map_id").groupby("steamid").tail(n_last)
    return result
