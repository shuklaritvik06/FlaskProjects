from flask import Flask, jsonify
import aiohttp

app = Flask(__name__)


async def fetch_data():
    async with aiohttp.ClientSession() as session:
        async with session.get("url") as response:
            return await response.json()


@app.route("/")
async def index():
    data = await fetch_data()
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
