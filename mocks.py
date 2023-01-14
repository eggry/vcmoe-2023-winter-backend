import json
def mock_all_fav_videos(fav_id):
    with open("mock_data/fav_list.json",encoding="utf-8") as f:
        return json.load(f)