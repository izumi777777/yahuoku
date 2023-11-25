# ========================================================
# ライブラリ宣言
# ========================================================
from flask import Flask, render_template, request, jsonify, Response
import os
import time
import csv
import requests
from io import StringIO
from bs4 import BeautifulSoup
from openpyxl import Workbook
from threading import Thread

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# 商品情報を保持するリスト
products_info = []

@app.route('/search', methods=['POST'])
def search():
    global products_info
    keyword = request.form['keyword']

    # ここにPythonスクリプトの内容をコピー
    base_url = 'https://auctions.yahoo.co.jp/closedsearch/closedsearch?p=' + keyword + '&n=100';
    print(base_url)
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

# =======================================================
# Excelファイルを作成し、シートを取得する
# =======================================================
    wb = Workbook()
    sheet = wb.active

    # ヘッダー行を書き込む
    sheet.append(['日付', '商品名', '落札価格', '商品URL'])

# ========================================================
# 取得したリンクを解析し、日付、商品名、落札価格を取得する
# ========================================================
    url_count = len(urls_to_parse)
    print("URLの個数は: ", url_count, "個です。")
    print(urls_to_parse[0])
    count = 0 # 繰り返し回数
    datetime = []
    product_name = []


    while count < url_count:
        for url in urls_to_parse:
            print(url)
            response = requests.get(urls_to_parse[count])  # タプルからURLを取り出す
            print(response)
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            count += 1  # countにプラス1
            
            time.sleep(2)
            # 取得したリンクから日付、商品情報、落札価格を取得する
            # 取得したリンクから日付、商品情報、落札価格を取得する
            items = soup.find_all('li', class_='Product')  # 商品情報を取得する変数を修正
            for item in items:
                # 日付の取得
                datatime = item.find('span', class_='Product__time').text.strip()
                # print(datatime)
                raw_datetime = datatime
                # スペースで文字列を分割して日付部分だけを取り出す
                date_only = raw_datetime.split(' ')[0]
                print(date_only)
            
                # 商品名の取得
                name = item.find('a', class_='Product__titleLink').text.strip()
                print(name) # 取得した商品名の確認
            
                # 落札価格の取得
                price = item.find('span', class_='Product__priceValue').text.strip()
                print("落札価格は: ", price, "円でした。") # 取得した落札価格の確認
            
                # リンクの取得
                link = item.find('a', class_='Product__titleLink')['href']
                print("取得したリンク: ", link) # 取得したリンクの確認
                
                # 商品情報をリストに追加
                products_info.append({
                    'date': date_only,
                    'name': name,
                    'price': price,
                    'url': link
                })
                
                # 商品情報を書き込む
                sheet.append([date_only, name, price, link])
                time.sleep(1)
                
                # 商品情報の変数を初期化
                date_only = ""
                name = ""
                price = ""
                link = ""
                print(date_only)
                print(name)
                print(price)
                print(link)
                
            # Excelファイルを保存する
            # 変数にファイル名を格納
            print(keyword)
            keyword = keyword.replace(" ", "_").replace("　", "_")
            print(keyword)
            file_name = f"{keyword}_test_yahuokulist.xlsx"
            wb.save(file_name)
            print(file_name)
    print("Excelファイルの保存が完了しました")

    # 商品情報を結果ページに渡す
    return render_template('result.html', keyword=keyword, items=products_info)

@app.route('/download_csv', methods=['GET'])
def download_csv():
    global products_info

    # CSVデータを生成
    csv_data = generate_csv(products_info)

    # ダウンロード用のレスポンスを作成
    response = Response(csv_data, content_type='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=products_info.csv'

    return response

def generate_csv(data):
    # CSVデータを生成する関数
    csv_data = StringIO()
    csv_writer = csv.writer(csv_data)

    # ヘッダー行を追加
    csv_writer.writerow(['日付', '商品名', '落札価格', '商品URL'])

    # データ行を追加
    for item in data:
        csv_writer.writerow([item['date'], item['name'], item['price'], item['url']])

    return csv_data.getvalue()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
