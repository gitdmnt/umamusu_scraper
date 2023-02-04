import requests
import json
import time
import shaper


# スクレイパー部分


def scrape_pixiv(scraper_type):
    if scraper_type == "search":
        # (検索結果は複数ページに渡るので)全てのページを探索してIDをかき集める部分
        return search_pixiv

    elif scraper_type == "collect":
        # 各イラストIDについて、全てのページを開いてデータをかき集める部分
        return collect_data


def scrape_umamusume():
    name_container = []
    for i in range(1, 3):
        time.sleep(1)
        url = "https://umamusume.jp/app/wp-json/wp/v2/character?per_page=100&page=" + \
            str(i)
        response = requests.get(url)
        json_response = json.loads(response.text)
        name_container += shaper.collect_uma_name(json_response)
    return name_container


def search_pixiv(tags, term):
    print("collecting illustration ID from " + shaper.join_tags(tags) + "...")

    urls = url_encoder("pixiv_search")(tags, term)
    json_data = []

    for url in urls:
        time.sleep(2)
        response = requests.get(url)
        json_response = json.loads(response.text)
        json_data.append(json_response)
    id_container = shaper.collect_id(json_data)

    print("ID collection completed")
    return id_container


def collect_data(id_container):
    print("collecting data from illustrations")

    status_container = []
    for i, id in enumerate(id_container):
        print("requesting data of ID " + id +
              "... (" + str(i + 1) + "/" + str(len(id_container)) + ")")
        time.sleep(2)
        url = url_encoder("pixiv_collect")(id)
        response = requests.get(url)
        json_response = json.loads(response.text)
        status = shaper.read_status(json_response)
        status_container.append(status)

    print("data collection completed")
    return status_container

# URLエンコーダー部分


def url_encoder(encoder_type):
    if encoder_type == "pixiv_search":
        return search_url_encoder

    elif encoder_type == "pixiv_collect":
        return collect_url_encoder


def search_url_encoder(tags, term):
    start_date = term[0]
    end_date = term[1]
    search_word = shaper.join_tags(tags)
    # まず1ページ目にアクセスしてtotalを取得
    total = int(json.loads(requests.get("https://www.pixiv.net/ajax/search/artworks/" + search_word + "?word=" + search_word +
                "&order=date_d&mode=all&scd=" + start_date + "&ecd=" + end_date + "&p=1&s_mode=s_tag&type=all").text)["body"]["illustManga"]["total"])
    max_page = total // 60 + 1
    urls = []
    # pだけ変えたurlを用意
    for i in range(1, max_page + 1):
        url = "https://www.pixiv.net/ajax/search/artworks/" + search_word + "?word=" + search_word + "&order=date_d&mode=all&scd=" + start_date + \
            "&ecd=" + end_date + "&p=" + str(i) + "&s_mode=s_tag&type=all"
        urls.append(url)
    return urls


def collect_url_encoder(id):
    url = "https://www.pixiv.net/ajax/illust/" + id
    return url
