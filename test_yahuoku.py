import os  # ファイル操作用
import openpyxl  # Excel操作用
import time
import requests  # Webサイト情報の取得用
from bs4 import BeautifulSoup  # Webサイト情報の取得用

# ========================================================
# 静的解析対象Webサイトの初期URLを宣言
# ========================================================
# 取得したいヤフオクの落札相場のURLを入力する
# base_url = input("落札相場を取得したヤフオクのURLを入力してください: ")
base_url = "https://auctions.yahoo.co.jp/closedsearch/closedsearch?va=ONKYO+FR-N7&b=1&n=100&auccat=&tab_ex=commerce&ei=utf-8&aq=-1&oq=&sc_i=&exflg=&p=ONKYO+FR-&x=0&y=0"
print("1回目のURL : " + base_url)

# ========================================================
# 静的解析対象の初期Webページからリンクを取得する
# ========================================================

# URLを格納するリストを初期化
urls_to_parse = [base_url]

while True:
    # 取得してきたWebサイトのHTMLを格納する変数を宣言
    response = requests.get(urls_to_parse[-1])
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup)

    # a要素を検索し、"次へ"の文字列を含んでいるか確認
    cheack_element = soup.find('a', class_='Pager__link', attrs={'data-cl-params': True, 'href': True}, string='次へ')

    if cheack_element:
        next_page_url = cheack_element['href']
        urls_to_parse.append(next_page_url)
        print("次へのURL:", next_page_url)

        # サーバへの負担を減らすために一時停止
        time.sleep(2)
    else:
        print("次へのリンクが見つかりませんでした。")
        break
print(urls_to_parse)
print("次へのリンクの数: ", len(urls_to_parse), "個")

        # 取得したリンクを解析し、それぞれ日付、商品名、落札価格を取得する
        # ...

        # 解析が終了したら次のURLへ移る