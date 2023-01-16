from config import HOST_UID
import re


def parse_election(reply):
    if str(reply["mid"]) == HOST_UID:
        if res := re.match(
            r"^【(.*)】(\d+)进(\d+)", reply["content"]["message"]
        ):
            title = res[0]
            group = res[1]
            count = res[2]
            final = res[3]
            videos = re.findall(r"([0-9A-Z]+)[\. ](.*av[\d/]*)",
                                reply["content"]["message"])
            jump_url = reply["content"]["jump_url"]
            videos = [{"idx": idx, "avid": jump_url[url]['click_report'],
                       "title":jump_url[url]['title']} for idx, url in videos]
            return ({
                "rpid": reply["rpid"],
                "title": title,
                "group": group,
                "count": count,
                "final": final,
                "videos": videos,
            })
    return None


def parse_vote(reply):
    message = reply["content"]["message"]
    votes = message.split() if re.match(r"^[A-Z0-9 ]+$", message) else []
    result = {
        "message": message,
        "ctime": reply["ctime"],
        "user": reply["member"]["uname"],
        "votes": votes
    }
    return result
