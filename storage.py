import json
from datetime import datetime
import os

__data_dir = os.getenv("VC_MOE_DATA_DIR", "./data")

if not os.path.exists(__data_dir):
    os.makedirs(__data_dir)

print(f"Data dir: {__data_dir}")


def dump_to_json(tag, data):
    timecode = datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    with open(f"{__data_dir}/dump-{tag}-{timecode}.json", "w", encoding="utf-8") as f:
        json.dump(data, f)