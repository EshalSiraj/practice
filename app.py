import os
from flask import Flask, jsonify
import redis

app = Flask(__name__)

APP_MODE = os.getenv("APP_MODE", "development")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

cache = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True,
    socket_connect_timeout=2,
)

@app.route("/")
def home():
    try:
        visits = cache.incr("visits")
        redis_status = "connected"
    except redis.RedisError:
        visits = None
        redis_status = "unavailable"

    return jsonify({
        "message": "DevOps midterm practice app",
        "app_mode": APP_MODE,
        "redis_status": redis_status,
        "visit_count": visits,
    })

@app.route("/health")
def health():
    return jsonify({"status": "ok", "app_mode": APP_MODE})

if __name__ == "__main__":
    # Listen on all interfaces so Docker port publishing can reach the app.
    app.run(host="0.0.0.0", port=5000)
