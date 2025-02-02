import sqlite3
import polars as pl
from datetime import datetime, timedelta
from ipodnano_scrobbler.scrobble import login, scrobble
from trainerlog import get_logger
LOGGER = get_logger("ipod-nano-scrobbler")
import time
from pathlib import Path
import pandas as pd
import tqdm

def mac_absolute_time_to_datetime(mac_timestamp):
    mac_epoch = datetime(2001, 1, 1, 0, 0, 0)
    return mac_epoch + timedelta(seconds=mac_timestamp)

def one_month_ago(days=30):
    now = datetime.now()
    return now - timedelta(days=days)

def get_play_counts(ipod_path, days=30):
    dynamic_itdb = (Path(ipod_path) / "Dynamic.itdb").absolute()
    library_itdb = (Path(ipod_path) / "Library.itdb").absolute()

    conn_dynamic = sqlite3.connect(dynamic_itdb, cached_statements=2000)
    conn_library = sqlite3.connect(library_itdb, cached_statements=2000)
    dynamic_info = pd.read_sql_query("SELECT * FROM item_stats", conn_dynamic)
    dynamic_info = pl.from_pandas(dynamic_info)
    track_properties = pd.read_sql_query("SELECT * FROM item", conn_library)
    track_properties = pl.from_pandas(track_properties)
    conn_library.close()
    conn_dynamic.close()

    dynamic_info = dynamic_info.with_columns(pl.col("date_played").map_elements(lambda timestamp: mac_absolute_time_to_datetime(timestamp)))
    track_properties = track_properties.select("pid", "title", "album", "artist")
    dynamic_info = dynamic_info.rename({"item_pid": "pid"})

    play_counts = dynamic_info.join(track_properties, on="pid")
    play_counts = play_counts.select("pid", "play_count_user", "play_count_recent", "date_played", "title", "album", "artist")
    play_counts = play_counts.filter(pl.col("date_played") >= one_month_ago(days))
    play_counts = play_counts.filter(pl.col("play_count_recent") >= 1)
    return play_counts.sort("date_played")

def reset_recent_plays(ipod_path):
    LOGGER.info(f"Set recent play counts to 0")
    dynamic_itdb = (Path(ipod_path) / "Dynamic.itdb").absolute()
    conn_dynamic = sqlite3.connect(dynamic_itdb)
    cursor = conn_dynamic.cursor()
    cursor.execute("UPDATE item_stats SET play_count_recent = 0;")
    conn_dynamic.commit()
    conn_dynamic.close()

def main():
    import argparse
    parser = argparse.ArgumentParser(prog='ipod-nano-scrobbler')
    parser.add_argument('--ipod_path', required=True, type=str)
    parser.add_argument('--skipcount', default=30, type=int, help='Skip songs with this or more recent plays')
    parser.add_argument('--days', default=30, type=int, help='Skip playcounts older than this')
    args = parser.parse_args()
    LOGGER.debug(f"Args: {args}")
    LOGGER.info(f"Setup last.fm login...")
    SESSION_KEY, LAST_FM_API, LAST_FM_API_SECRET = login()
    LOGGER.info(f"Get iTunes database from {args.ipod_path}...")
    play_counts = get_play_counts(args.ipod_path, days=args.days)
    play_counts = play_counts.filter(pl.col("play_count_recent") < args.skipcount)
    recent_counts_total = play_counts.select("play_count_recent").sum().item()
    if recent_counts_total > len(play_counts):
        LOGGER.warning("Some tracks were played multiple times recently. Some of the play times need to be imputed.")
    
    LOGGER.info(f"Scrobbling {recent_counts_total} recent plays of {len(play_counts)} tracks...")
    for track in tqdm.tqdm(play_counts.rows(named=True)):
        title, artist = track["title"], track["artist"]
        last_played = track["date_played"]
        recent_playcount = track["play_count_recent"]
        LOGGER.debug(f"Scrobble {title}, {artist}, {recent_playcount} times")
        for ix in range(recent_playcount):
            imputed_date = last_played-timedelta(days=ix)
            if imputed_date >= one_month_ago(days=args.days):
                LOGGER.debug(f"Scrobble {title}, {artist}, {imputed_date}")
                
                date_timestamp = str(int(imputed_date.timestamp()))

                response = scrobble(title, artist, SESSION_KEY, LAST_FM_API, LAST_FM_API_SECRET, timestamp=date_timestamp)
                assert response.status_code == 200, f"Scrobbling status not ok {response.status_code}"
                time.sleep(0.05)
            else:
                LOGGER.debug(f"Skip since imputed date {imputed_date} is further away than {args.days} days")

        time.sleep(1)

    if len(play_counts) >= 1:
        reset_recent_plays(args.ipod_path)
    else:
        LOGGER.info(f"No recent play counts to be reset")


if __name__ == '__main__':
    main()