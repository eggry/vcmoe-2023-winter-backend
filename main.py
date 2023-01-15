from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apis import assign_group, assign_page, get_all_fav_video, get_draw_result, shuffle_with_seed,get_fav
from mocks import mock_all_fav_videos

app = FastAPI()

origins = [
    "https://localhost:8080",
    "http://localhost:8081",
    "https://xiaohengshu.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/mock/fav/{fav_id}")
def list_fav_video(fav_id: int, shuffle: bool = False, seed: Optional[int | str] = None):
    print(
        f"[MOCK] fav request. id: {fav_id}, shuffle: {shuffle}, seed: {seed}, seed_type: {type(seed).__name__}")
    videos = mock_all_fav_videos(fav_id)
    if (shuffle):
        shuffle_with_seed(videos, seed)
    return videos

@app.get("/fav")
def list_fav():
    print("fav request.")
    fav_list = get_fav(495775367)
    return fav_list["data"]["list"]

@app.get("/fav/{fav_id}")
def list_fav_video(fav_id: int, shuffle: bool = False, seed: Optional[int | str] = None, page_size: Optional[int] = None):
    print(
        f"fav video request. id: {fav_id}, shuffle: {shuffle}, seed: {seed}, seed_type: {type(seed).__name__}")
    videos = get_all_fav_video(fav_id)
    if shuffle:
        shuffle_with_seed(videos, seed)
    if page_size and page_size > 0:
        assign_page(videos, page_size)
    return videos

@app.get("/group/{group_id}")
def list_group_result(group_id:int,perfer_size:int):
    videos = get_draw_result(group_id)
    assign_group(videos,10)
    return videos