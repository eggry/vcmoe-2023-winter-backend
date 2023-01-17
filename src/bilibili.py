from math import ceil
from utils import get_json_from_url
from storage import dump_data

__list_favorites_api = "https://api.bilibili.com/x/v3/fav/folder/created/list-all?up_mid={mid}"

__list_favorite_videos_by_page_api = "https://api.bilibili.com/x/v3/fav/resource/list?media_id={fvid}&ps={ps}&pn={pn}"

__list_video_replies_by_page_api = "https://api.bilibili.com/x/v2/reply?type=1&oid={avid}&pn={pn}&ps={ps}&sort=0"

__list_reply_replies_by_page_api = "https://api.bilibili.com/x/v2/reply/reply?type=1&oid={avid}&root={rpid}&pn={pn}&ps={ps}"


def list_favorites(mid):
    print(f"list favorites: mid: {mid}")
    url = __list_favorites_api.format(mid=mid)
    result = get_json_from_url(url)
    dump_data("list_favorites", {"result": result, "mid": mid, })
    return result


def list_favorite_videos_by_page(fvid, pn=1, ps=20):
    print(f"list favorite videos by page: fvid: {fvid}, pn: {pn}, ps: {ps}")
    url = __list_favorite_videos_by_page_api.format(fvid=fvid, pn=pn, ps=ps)
    result = get_json_from_url(url)
    dump_data("list_favorite_videos_by_page", {
              "result": result, "fvid": fvid, "pn": pn, "ps": ps, })
    return result


def list_video_replies_by_page(avid, pn=1, ps=49):
    print(f"list video replies by page: avid: {avid}, pn: {pn}, ps: {ps}")
    url = __list_video_replies_by_page_api.format(avid=avid, pn=pn, ps=ps)
    result = get_json_from_url(url)
    dump_data("list_video_replies_by_page", {
              "result": result, "avid": avid, "pn": pn, "ps": ps, })
    return result


def list_reply_replies_by_page(avid, rpid, pn=1, ps=20):
    print(
        f"list reply replies by page: avid: {avid}, rpid: {rpid}, pn: {pn}, ps: {ps}")
    url = __list_reply_replies_by_page_api.format(
        avid=avid, rpid=rpid, pn=pn, ps=ps)
    result = get_json_from_url(url)
    dump_data("list_reply_replies_by_page", {
              "result": result, "avid": avid, "rpid": rpid, "pn": pn, "ps": ps, })
    return result


def list_reply_replies(avid, rpid):
    r = list_reply_replies_by_page(avid, rpid)
    total = r["data"]["page"]["count"]
    page_size = r["data"]["page"]["size"]
    replies = r["data"]["replies"]
    if not replies:
        replies=[]
    root = r["data"]["root"]
    total_page_size = ceil(total/page_size)
    for i in range(2, total_page_size+1):
        r = list_reply_replies_by_page(avid, rpid, pn=i)
        replies += r['data']['replies']
        root = r["data"]["root"]
    dump_data("list_favorite_videos", {
              "replies": replies, "root": root, "fvid": rpid})
    return replies, root


def list_favorite_videos(fvid):
    page_size = 20

    r = list_favorite_videos_by_page(fvid)
    total = r['data']['info']['media_count']
    result = r['data']['medias']

    if not result:
        return []

    total_page_size = ceil(total/page_size)

    for i in range(2, total_page_size+1):
        r = list_favorite_videos_by_page(fvid, i, page_size)
        result += r['data']['medias']

    actual_total = len(result)

    print(
        f"fav all video count: fvid: {fvid}, count: {total}, actual:{actual_total}")

    dump_data("list_favorite_videos", {
              "result": result, "fvid": fvid})

    return result
