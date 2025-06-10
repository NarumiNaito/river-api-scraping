import json, traceback
from flask import Flask, Response
from flask_cors import CORS
from scraper import get_water_data

app = Flask(__name__)
CORS(app)

@app.route("/api/water-level", methods=["GET"])
def water_level():
    try:
        return get_water_data()  
    except Exception as e:
        import traceback
        err = {
            "error": str(e),
            "trace": traceback.format_exc()
        }
        payload = json.dumps(err, ensure_ascii=False)
        return Response(payload, status=500, mimetype="application/json; charset=utf-8")
        
if __name__ == "__main__":
    print("Starting Flask")
    app.run(debug=True, host="0.0.0.0", port=5001)
