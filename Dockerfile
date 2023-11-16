# ベースイメージの指定
FROM python:3.10.9

# 作業ディレクトリの設定
WORKDIR /app

# 必要なファイルをコピー
COPY requirements.txt .
COPY dev-yahuokuscraiping.py .

# パッケージのインストール
RUN pip install --no-cache-dir -r requirements.txt

# スクリプトの実行
CMD ["python", "dev-yahuokuscraiping.py"]
