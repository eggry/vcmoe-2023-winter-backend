"""
Author: Eggry
URL: https://github.com/eggry/BiliReplyDetailCrawler
License: MIT License
"""

import random
from math import ceil
from typing import MutableSequence
import requests

from dump import dump_to_json

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


def shuffle_with_seed(items: MutableSequence, seed):
    print(
        f"shuffle with seed. len: {len(items)}, seed: {seed}, seed_type:{type(seed).__name__}")
    random.Random(seed).shuffle(items)

    dump_to_json(f"shuffle_{type(seed).__name__}_{seed}",items)
