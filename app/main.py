import json, traceback, threading, time, os
from flask import Flask, jsonify, Response
from flask_cors import CORS
from scraper import get_water_data
from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv("FLASK_PORT", 5001))
SCRAPE_INTERVAL_SECONDS = int(os.getenv("SCRAPE_INTERVAL_SECONDS", 300))  

app = Flask(__name__)

CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS").split(",")
CORS(app, resources={r"/api/*": {"origins": CORS_ALLOWED_ORIGINS}})

cached_data = None
cached_lock = threading.Lock()

def update_data_periodically():
    global cached_data
    try:
        print("初回データ取得中...")
        data = get_water_data()
        with cached_lock:
            cached_data = data
        print("初回データ取得完了")
    except Exception as e:
        print("初回データ取得エラー:", str(e))

    while True:
        start_time = time.time()
        try:
            print("水位データの更新中...")
            data = get_water_data()
            with cached_lock:
                cached_data = data
            print("水位データの更新")
        except Exception as e:
            print("水位データの更新エラー:", str(e))
        elapsed = time.time() - start_time
        time.sleep(max(SCRAPE_INTERVAL_SECONDS - elapsed, 0))


@app.route("/api/water-level", methods=["GET"])
def water_level():
    with cached_lock:
        if cached_data:
            return jsonify(cached_data)
    return Response(
        json.dumps({"error": "データがまだ取得されていません"}, ensure_ascii=False),
        status=503,
        mimetype="application/json; charset=utf-8"
    )

if __name__ == "__main__":
    print("Starting Flask with background updater...")
    threading.Thread(target=update_data_periodically, daemon=True).start()
    app.run(debug=False, host="0.0.0.0", port=PORT)
