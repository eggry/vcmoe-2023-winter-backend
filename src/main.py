import numpy as np
import pandas as pd
from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import bilibili
import config
import seq
from storage import dump_data
import utils
import election

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/favorites")
def list_favorites():
    print("proccess list favorites request.")
    favorites = bilibili.list_favorites(config.HOST_UID)
    result = favorites["data"]["list"]
    dump_data("api_list_favorites", {"result": result})
    return result


@app.get("/favorites/{fvid}")
def list_favorite(fvid: int):
    result = bilibili.list_favorite_videos(config.HOST_UID, fvid)
    seq.assign_idx(result)
    dump_data("api_list_favorite", {"result": result, "fvid": fvid})
    return result


@app.get("/favorites/{fvid}/groups")
def list_groups(
        fvid: int,
        perfer_size: int,
        shuffle_seed: Optional[int | str] = None):
    result = bilibili.list_favorite_videos(config.HOST_UID, fvid)

    seq.shuffle_with_seed(result, shuffle_seed)

    seq.assign_group(result, perfer_size)

    dump_data("api_list_groups", {"result": result, "fvid": fvid,
              "perfer_size": perfer_size, "shuffle_seed": shuffle_seed})
    return result


@app.get("/elections")
def list_elections():
    min_timestamp = utils.days_delta_timestamp(-3)
    replies = []
    for pn in range(1, 30):
        r = bilibili.list_video_replies_by_page(config.HOST_AVID, pn)
        replies += r["data"]["replies"]
        last_timestamp = replies[-1]['ctime']
        if last_timestamp <= min_timestamp:
            break
    elections = []
    for reply in replies:
        if ele := election.parse_election(reply):
            elections.append(ele)
    dump_data("api_list_elections", {
              "elections": elections, "replies": replies})
    return elections


@app.get("/elections/{rpid}/votes")
def list_votes_in_reply(rpid: int):
    votes = []
    replies, root = bilibili.list_reply_replies(config.HOST_AVID, rpid)
    if ele := election.parse_election(root):
        votes = list(map(election.parse_vote, replies))
    dump_data("api_list_votes_in_reply", {
              "votes": votes, "replies": replies, "root": root, "rpid": rpid, "election": ele})
    return votes


@app.get("/elections/{rpid}/result")
def get_election_result(rpid: int):
    result = []
    replies, root = bilibili.list_reply_replies(config.HOST_AVID, rpid)
    if ele := election.parse_election(root):
        votes = list(map(election.parse_vote, replies))
        vote_values = []
        for vote in votes:
            vote_values += vote["votes"]
        vote_counts = pd.Series(vote_values).value_counts()
        vote_counts.name = "votes"
        df = pd.DataFrame(ele["videos"]).merge(
            vote_counts, left_on="idx", right_index=True, how="left")
        df = df.fillna(0)
        df = df.astype({"votes": np.int64})
        result = df.to_dict(orient='records')
    dump_data("api_get_election_result", {
              "result": result, "replies": replies, "root": root, "rpid": rpid, "election": ele})
    return result
