import requests
from datetime import datetime, timedelta, timezone


def current_CST_timecode():
    return datetime.now(timezone(timedelta(hours=8))).strftime('%Y%m%d-%H%M%S-%f')


def days_delta_timestamp(daysdelta):
    dt = datetime.now() + timedelta(days=daysdelta)
    return dt.timestamp()


def get_json_from_url(url):
    r = requests.get(url)
    r.raise_for_status()
    return r.json()
