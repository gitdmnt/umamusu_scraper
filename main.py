import scraper
import shaper
# タグ関連を設定
character_list = scraper.scrape_umamusume()
series_name = "ウマ娘"
common_tags = []

# 日付を指定
start_date = "2023-01-01"
end_date = "2023-01-02"


term = [start_date, end_date]

# [["アグネスタキオン(ウマ娘)", "かわいい", "麗しい"], ["マンハッタンカフェ(ウマ娘)", "かわいい", "麗しい"]]
tag_list = shaper.shape_tags(character_list, series_name, common_tags)
df_container = []

for tags in tag_list:
    # 各検索単語に関して、まずはillustIDをjson_dataから取り出す

    id_container = scraper.scrape_pixiv("search")(
        tags, term)  # [ID1, ID2, ... IDn]

    status_container = scraper.scrape_pixiv("collect")(
        id_container)  # [dic1, dic2, ... dicn]
    # dicn = {"bookmark": int, "view": int, "AI": bool, "R-18": bool, "date": yyyy-MM-dd}

    df = shaper.shape_status(status_container)
    df_container.append(df)
    df.to_csv("data/" + shaper.join_tags(tags) + "_" +
              start_date + "_" + end_date + ".csv")
    print(df)
# ここまで

# これ各ステップで一気にやってるけど、search_wordごとに各ステップをやる方がコードが落ち着いて見える気がしてきた


# result_list = scraper.shape_result(data)

# csv = scraper.create_csv(result_list)

# export(csv)

# create_bcr(csv)

"""
"https://www.pixiv.net/ajax/search/artworks/" + tag + "?word=" + tag + "&order=date_d&mode=all&scd=" + start_date + "&ecd=" + end_date
のtotalの値を見れば作品数がわかる

https://www.pixiv.net/ajax/search/artworks/ <tags> ?word= <tags> &order=date_d&mode=all&scd= <start_date> &ecd= <end_date> &p= <page_number> &s_mode=s_tag&type=all&lang=ja&version=9c834eede9446d61102731a4be356cd0f1090e84
tagsはスペース区切り
dateはyyyy-MM-dd
page_numberは1-indexed
のbody: illustManga: data: total:の値を見れば作品数がわかる
body: illustManga: data: n: id: からidを取得できる (0<=n<=59)

https://www.pixiv.net/ajax/illust/ + (作品ID) からjsonを取得して、
body: bookmarkCountとかbody: viewCountの値を見れば閲覧数とかがわかる
body: aiType からAIかどうかを判定できる(1: 非AI, 2: AI)
body: xRestrict からR-18かどうかを判定できる(0: 一般、1: R-18)
body: createDateによって作成日を見られるyyyy-MM-dd(この後にT……と時間とかが続くけど切り捨ててよさそう)

フロー

# 前処理
検索条件を決める

# スクレイピング
検索によって作品数totalを得る
作品数からページ数pを得る
各検索ページからイラストIDidとAIかどうかaiTypeを得てリストを作成
各IDについてアップロード日createDateとブックマーク数bookmarkCount, 閲覧数viewCount, R指定xRestrictをリストに追加


# データの加工
取得したデータをpandasでクネクネ
指定された期間ごとに色々やる
- 作品数の推移をみる ← これもうやったからええか、面倒でもあるし
- 閲覧数やブックマーク数の合計、平均、中央値、最大値、(標準偏差)など
- キャラごとにAI絵の割合を出す
- R-18の割合を出す
- R-18におけるAI絵の占める割合を出す
- ai絵とそれ以外の評価の差とかは？

# 出力
csvに出力(これ無駄なスクレイピングを防ぐために一応用意しとくべき)
bar_chart_raceで可視化して遊ぶ
- 合計閲覧数レースやるべき
- どれの需要が不足しているのかとか知りたいよな、どうしたらわかるんだろう
matplotlibで可視化して遊ぶ
- 平均ブクマ数の高い順10人
- 平均閲覧数の高い順10人
- ai絵の割合グランプリ
- R-18割合グランプリ
- R-18枚数グランプリ

"""
