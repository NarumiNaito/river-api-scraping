FROM python:3.11-slim

# 環境変数設定
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 必要なパッケージのインストール
RUN apt-get update && apt-get install -y \
    curl unzip gnupg2 wget \
    chromium-driver \
    chromium \
    fonts-ipafont-gothic \
    --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Selenium が Chromium を使うように設定
ENV CHROME_BIN=/usr/bin/chromium

# 作業ディレクトリ作成
WORKDIR /app

# requirements.txt をコピーしてインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードをコピー
COPY app/ .

# ポート解放
EXPOSE 5001

# Flaskアプリ起動
CMD ["python", "main.py"]
CMD ["sh", "-c", "echo Starting Flask && python main.py"]
