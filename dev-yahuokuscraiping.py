# ========================================================
# ライブラリの宣言スペース
# ========================================================
import os  # ファイル操作用
import time # time.sleep()のために必要
import requests  # Webサイト情報の取得用
from bs4 import BeautifulSoup  # Webサイト情報の取得用

# ========================================================
# 静的解析対象Webサイトの初期URLを宣言
# ========================================================
# 取得したい相場のURLを入力する
# base_url = input("相場を取得したヤフオクのURLを入力してください: ")
base_url = "https://auctions.yahoo.co.jp/closedsearch/closedsearch?va=ONKYO+FR-N7&b=1&n=100&auccat=&tab_ex=commerce&ei=utf-8&aq=-1&oq=&sc_i=&exflg=&p=ONKYO+FR-&x=0&y=0"
print("1回目のURL : " + base_url)

# ========================================================
# HTML取得
# ========================================================
response = requests.get(base_url)
html = response.text

# ========================================================
# 静的解析対象の初期Webページからリンクを取得する
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
        # if index < len(href_elements):
        urls_to_parse.append(href_value)
            
        # サーバへの負担を減らすために一時停止
        time.sleep(2)
# ========================================================
# 最後の要素のURLに次へのリンクがあるかチェック
# ========================================================
    del urls_to_parse[-1] # 最後の要素を削除
    print(urls_to_parse) # リストの要素を確認
    
    check_url = urls_to_parse[-1] # 最後の要素のURLを取得
    print("最後のURL: ", check_url) # 最後のURLが取得できているか確認
    
    response = requests.get(check_url) # 最後のURLのHTMLを取得
    check_url_html = response.text # 取得したHTMLを格納
    soup_check_html = BeautifulSoup(check_url_html, 'html.parser') # HTMLを解析
    print(soup_check_html) # HTMLを表示
    
    next_page_url = [] # 次へのURLを格納するリストを初期化
    
    # a要素を検索し、"次へ"の文字列を含んでいるか確認
    cheack_element = soup_check_html.find('a', class_='Pager__link', attrs={'data-cl-params': True, 'href': True}, string='次へ')

    if cheack_element:
        next_page_url.append(cheack_element['href'])
        print("次へのURL:", next_page_url)
    else:
        print("次へのリンクが見つかりませんでした。")
    
    # 取得したURLを順番に解析
    for index, url in enumerate(urls_to_parse, start=1):
        print(f"{index}回目の解析開始: {url}")
        # サーバへの負担を減らすために一時停止
        time.sleep(2)
        # URLのHTMLを取得
        response = requests.get(url)
        html = response.text

        # HTMLを解析
        soup = BeautifulSoup(html, 'html.parser')
        # print(soup)
        # 解析した結果を使って何かしらの処理を行う
        # ...

        # 解析が終了したら次のURLへ移る