import json
import time
__data_dir = "/home/json_dump"

def dump_to_json(tag,data):
    with open(f"{__data_dir}/{tag}-{int(time.time())}.json","w",encoding="utf-8") as f:
        json.dump(data,f)