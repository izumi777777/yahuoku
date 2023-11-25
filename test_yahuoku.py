import os  # ファイル操作用
import time
import boto3
import requests  # Webサイト情報の取得用
from bs4 import BeautifulSoup  # Webサイト情報の取得用
from openpyxl import Workbook # Excel操作用

# ========================================================
# 静的解析対象Webサイトの初期URLを宣言
# ========================================================
# 取得したいヤフオクの落札相場のURLを入力する
keyword = input("落札相場を取得したいキーワードを入力してください: ")
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
        count += 1 # countにプラス1 
        
        # 取得したリンクを解析しする
        product_name = soup.find_all('li', class_='Product')
        print(product_name)
        time.sleep(2)
        # 取得したリンクから日付、商品情報、落札価格を取得する
        for item in product_name:
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
            
            # 商品情報を書き込む
            sheet.append([date_only, name, price, link])
            time.sleep(1)
        # Excelファイルを保存する
        # 変数にファイル名を格納
        print(keyword)
        keyword = keyword.replace(" ", "_").replace("　", "_")
        print(keyword)
        file_name = f"{keyword}_test_yahuokulist.xlsx"
        wb.save(file_name)
        print(file_name)
print("Excelファイルの保存が完了しました")

# ========================================================
# 作成したエクセルファイルをS3に転送
# ========================================================

# AWS Systems Managerのクライアントの作成
ssm = boto3.client('ssm')

# パラメーターストアからアクセスキーとシークレットキーを取得
access_key_parameter = ssm.get_parameter(Name='AuctionScraping-access_key', WithDecryption=True)
secret_key_parameter = ssm.get_parameter(Name='AuctionScraping-secret_key', WithDecryption=True)
    
aws_access_key_id = access_key_parameter['Parameter']['Value']
aws_secret_access_key = secret_key_parameter['Parameter']['Value']

# S3クライアントの作成
s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

# アップロード先のファイルパス
s3_path = '2023/11/'  # 任意のS3内のパス
s3_filepath = s3_path + file_name

# AWS S3にアップロード
bucket_name = 'yahuoku-scraping-files'
s3.upload_file(file_name, bucket_name, s3_filepath)
print("S3にファイルのアップロードが完了しました")