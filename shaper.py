import pandas as pd
import datetime

# タグを加工する部分


def shape_tags(character_list, series_name, common_tags):
    results = []
    for character in character_list:
        tags = [character + "(" + series_name + ")"]
        tags += common_tags
        results.append(tags)
    return results


def join_tags(tags):
    search_word = ""
    for tag in tags:
        search_word += tag + " "
    search_word = search_word[:len(search_word) - 1]
    return search_word

# jsonを加工する部分


def collect_id(json_data):
    id_container = []
    for detail in json_data:
        # illustIDを取り出す
        length = len(detail["body"]["illustManga"]["data"])
        # これだと1ページから1つしか取れてなくない？　そうじゃない
        for i in range(length):
            if "id" not in detail["body"]["illustManga"]["data"][i].keys():
                continue
            id = detail["body"]["illustManga"]["data"][i]["id"]
            id_container.append(id)
    return id_container


def collect_uma_name(json_data):
    length = len(json_data)
    name_container = []
    for i in range(length):
        name = json_data[i]["title"]["rendered"]
        name_container.append(name)
    return name_container


def read_status(json_response):
    body = json_response["body"]
    bookmark_count = int(body["bookmarkCount"])
    view_count = int(body["viewCount"])
    is_ai = False if body["aiType"] == 1 else True
    is_R18 = False if body["xRestrict"] == 0 else True
    upload_date = datetime.datetime.strptime(
        body["createDate"][:10], "%Y-%m-%d")
    status = {
        "bookmark": bookmark_count,
        "view": view_count,
        "AI": is_ai,
        "R-18": is_R18,
        "date": upload_date,
    }
    return status


def shape_status(status_container):
    df = pd.DataFrame(status_container)
    return df
