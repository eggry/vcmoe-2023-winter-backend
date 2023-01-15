import json
from config import DATA_DIR
from utils import current_CST_timecode
import os

DUMP_DIR = f"{DATA_DIR}/dump"
os.makedirs(DUMP_DIR, exist_ok=True)


def dump_data(tag, data):
    timecode = current_CST_timecode()
    with open(f"{DUMP_DIR}/{timecode}-{tag}.json", "w", encoding="utf-8") as f:
        json.dump(data, f)
