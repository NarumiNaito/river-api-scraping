# river-api-scraping

river の API です。
特定の河川情報を取得する為の API を提供します。

## 環境

- フレームワーク　: Flask
- 言語　: python

## 環境構築

下記の流れに従って、環境構築を行なってください。

#### clone

```
git clone git@github.com:NarumiNaito/river-api-scraping.git
```

#### build

```
docker compose build
```

#### コンテナ作成

```
docker compose up -d
```

#### コンテナへの接続

```
docker compose exec app /bin/sh
```
