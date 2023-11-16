# ========================================================
# ライブラリの宣言スペース
# ========================================================
import os  # ファイル操作用
import openpyxl  # Excel操作用
import time
import requests  # Webサイト情報の取得用
from bs4 import BeautifulSoup  # Webサイト情報の取得用

# ========================================================
# 静的解析対象Webサイトの初期URLを宣言
# ========================================================
# 取得したい相場のURLを入力する
# base_url = input("相場を取得したヤフオクのURLを入力してください: ")
base_url = "https://auctions.yahoo.co.jp/closedsearch/closedsearch?va=ONKYO+T-405&b=1&n=100&auccat=&tab_ex=commerce&ei=utf-8&aq=-1&oq=&sc_i=&exflg=&p=ONKYO+FR-N7&x=0&y=0"
print("1回目のURL : " + base_url)

# ========================================================
# HTML取得
# ========================================================
response = requests.get(base_url)
html = response.text

# ========================================================
# 静的解析対象の初期Webページから"次へ"ページがないか検索
# ========================================================

# URLを格納するリストを初期化
urls_to_parse = [base_url]

# 取得してきたWebサイトのHTMLを格納する変数を宣言
response = requests.get(base_url)
html = response.text
soup = BeautifulSoup(html, 'html.parser')
print(soup)

# 取得してきたWebサイトのHTMLを格納する変数を宣言
a_element = soup.find('a', class_='Pager__link', attrs={'data-cl-params': True}, href=True)

# <a>要素が存在すればhref属性を表示
if a_element:
    href_value = a_element['href']
    print(href_value)
    
    
    # または、find_allを使って複数の要素を取得することもできます
    href_elements = soup.find_all('a', class_='Pager__link', attrs={'data-cl-params': True, 'href': True})
    print("要素の数:", len(href_elements))
    # 各<a>要素からhref属性の値を取得
    for index, element in enumerate(href_elements, start=1):
        href_value = element['href']
        # print(f"{index}回目の出力: {href_value}")

        # 最後の要素以外を取得
        if index < len(href_elements):
            urls_to_parse.append(href_value)

    # 取得したURLを順番に解析
    for index, url in enumerate(urls_to_parse, start=1):
        print(f"{index}回目の解析開始: {url}")
        # URLのHTMLを取得
        response = requests.get(url)
        html = response.text

        # HTMLを解析
        soup = BeautifulSoup(html, 'html.parser')
        
        # 解析した結果を使って何かしらの処理を行う
        # ...

        # 解析が終了したら次のURLへ移る