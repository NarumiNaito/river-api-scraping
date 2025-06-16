FROM python:3.11-slim

# Chrome + ChromeDriver インストール（バージョン整合性取る）
RUN apt-get update && apt-get install -y \
    curl unzip gnupg2 wget \
    chromium \
    chromium-driver \
    fonts-ipafont-gothic \
    --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# PATH など明示的に設定（重要！）
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

EXPOSE 5001

CMD ["python", "main.py"]
