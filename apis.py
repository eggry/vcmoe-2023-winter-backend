"""
Author: Eggry
URL: https://github.com/eggry/BiliReplyDetailCrawler
License: MIT License
"""

import random
from math import ceil
from typing import Dict, List, MutableSequence
import requests

from storage import dump_to_json,__data_dir

__fav_list = "https://api.bilibili.com/x/v3/fav/folder/created/list-all?up_mid={mid}"

__fav_video_list = "https://api.bilibili.com/x/v3/fav/resource/list?media_id={fvid}&ps={ps}&pn={pn}"


def get_fav(mid):
    print(f"getting fav list: mid: {mid}")
    request_url = __fav_list.format(mid=mid)
    r = requests.get(request_url)
    r.raise_for_status()
    r = r.json()
    dump_to_json(f"fav_{mid}",r)
    return r


def get_fav_video(fvid, pn=1, ps=20):
    print(f"getting fav videos: fvid: {fvid}, pn: {pn}, ps: {ps}")
    request_url = __fav_video_list.format(fvid=fvid, pn=pn, ps=ps)
    r = requests.get(request_url)
    r.raise_for_status()
    r = r.json()
    dump_to_json(f"fav_video_{fvid}_{pn}_{ps}",r)
    return r


def get_all_fav_video(fvid, ps=20):
    print(f"getting all fav videos: fvid: {fvid}, ps: {ps}")

    r = get_fav_video(fvid)

    count = r['data']['info']['media_count']
    favs = r['data']['medias']

    max_pn = ceil(count/ps)

    print(f"fav info: fvid: {fvid}, count: {count}, max_pn:{max_pn}")

    for i in range(2, max_pn+1):
        r = get_fav_video(fvid, i, ps)
        favs += r['data']['medias']

    count_actual = len(favs)

    print(
        f"fav all video count: fvid: {fvid}, count: {count}, actual:{count_actual}")

    assert count_actual == count

    dump_to_json(f"all_fav_video_{fvid}_{ps}",r)

    return favs
import json
def get_draw_result(files):
    with open(f"{__data_dir}/draw_result/1.json","r",encoding="utf-8") as f:
        return json.load(f)
    
def shuffle_with_seed(items: MutableSequence, seed):
    print(
        f"shuffle with seed. len: {len(items)}, seed: {seed}, seed_type:{type(seed).__name__}")
    random.Random(seed).shuffle(items)

    dump_to_json(f"shuffle_{type(seed).__name__}_{seed}",items)

def assign_page(items: List[Dict], page_size:int):
    print(
        f"assigning page. len: {len(items)}, page_size: {page_size}")
    
    for idx,item in enumerate(items):
        item["_page"]=(idx//page_size)+1
        item["_page_idx"]=(idx%page_size)+1

    dump_to_json(f"assign_page_{len(items)}_{page_size}",items)

def assign_group(items: List[Dict], prefer_size:int):
    print(
        f"assigning group. len: {len(items)}, prefer_size: {prefer_size}")

    group_count, extra = divmod(len(items), prefer_size)

    group_info_list=[]
    for group_idx in range(group_count):
        group_id = chr(65+group_idx)
        group_size = prefer_size+1 if group_idx<extra else prefer_size
        group_info_list.extend(
            {"_group_id": group_id, "_group_idx": item_idx}
            for item_idx in range(1,group_size+1)
        )

    for item,group_info in zip(items,group_info_list):
        item|=group_info

    dump_to_json(f"assign_group_{len(items)}_{prefer_size}",items)