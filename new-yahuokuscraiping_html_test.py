# ========================================================
# ライブラリの宣言スペース
# ========================================================
from bs4 import BeautifulSoup  # BeautifulSoupのインポート
import html  # htmlエスケープ用

# ========================================================
# HTML取得テスト
# ========================================================

html_string = '<a class="Pager__link" data-cl-params="_cl_vmodule:pagination;_cl_link:next;_cl_position:1;" href="https://auctions.yahoo.co.jp/closedsearch/closedsearch?p=ONKYO+T-405&amp;va=ONKYO+T-405&amp;b=101&amp;n=100">次へ</a>'

# HTMLエンティティをデコード
html_decoded = html.unescape(html_string)

soup = BeautifulSoup(html_decoded, 'html.parser')

# aタグを検索し、href属性の値を取得
a_element = soup.find('a', class_='Pager__link')
if a_element:
    href_value = a_element['href']
    print(href_value)