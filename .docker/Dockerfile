FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libxml2-dev \
    libxslt1-dev \
    libcurl4-openssl-dev \
    libssl-dev \
    libffi-dev \
    locales \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN sed -i '/ja_JP.EUC-JP/s/^# //g' /etc/locale.gen && \
    locale-gen && \
    update-locale LANG=ja_JP.EUC-JP

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
