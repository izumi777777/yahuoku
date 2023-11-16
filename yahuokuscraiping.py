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
base_url = "https://auctions.yahoo.co.jp/closedsearch/closedsearch?p=ONKYO+T-405&va=ONKYO+T-405&b=1&n=100"
print("1回目のURL : " + base_url)

# ========================================================
# 静的解析対象の初期Webページから"次へ"ページがないか検索
# ========================================================
while True:
    # 取得してきたWebサイトのHTMLを格納する変数を宣言
    response = requests.get(base_url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    # 取得してきたWebサイトのHTMLを格納する変数を宣言
    a_element = soup.find('a', class_='Pager__link', attrs={'data-cl-params': True}, href=True)

    # <a>要素が存在すればhref属性を表示
    if a_element:
        href_value = a_element['href']
        print(href_value)
    
    # または、find_allを使って複数の要素を取得することもできます
    href_elements = soup.find_all('a', class_='Pager__link', attrs={'data-cl-params': True, 'href': True})
    print(href_elements[0])
    print(href_elements[1])
    print(href_elements[2])
    # 各<a>要素からhref属性の値を取得
    for element in href_elements:
        href_value = element['href']
        print(href_value)
    
    current_url = ""

    for txt in url_next_a:
        if '次へ' in txt.text:
            current_url = txt.get('href')
            print("2回目のURL : " + current_url)
            break
    # "次へ"のリンクが見つからないか、1回目のURLと同じ場合は終了
    if not '次へ' in txt.text or current_url == base_url:
        break  # "次へ"のリンクが見つからないか、1回目のURLと同じ場合は終了


    # 次のページのURLのHTMLを解析する
    response = requests.get(current_url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup)

# ========================================================
# 静的解析対象の初期Webページから"次へ"ページがないか検索
# ========================================================
# 取得してきたWebサイトのHTMLを格納する変数を宣言
    detail_url_list_b = soup.select('a')

    for txt in detail_url_list_b:
        if '次へ' in txt.text:
            current_url = txt.get('href')
            print("3回目のURL : " + current_url)
            break
        else:
            continue
        
    if not '次へ' in txt.text or current_url == base_url:
        break  # "次へ"のリンクが見つからないか、1回目のURLと同じ場合は終了

