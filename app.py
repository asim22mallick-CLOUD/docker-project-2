from flask import Flask
import redis

app = Flask(__name__)

cache = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True
)

@app.route("/")
def home():
    visits = cache.incr("visits")

    return f"""
    <h1>Docker Project 2</h1>
    <p>Multi-Container Application</p>
    <p>Visitor count: {visits}</p>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
