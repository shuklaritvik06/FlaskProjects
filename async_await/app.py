from flask import Flask, jsonify, g
import aiohttp


app = Flask(__name__)


# Callback function for URL defaults for all view functions of the application.
@app.url_defaults
def add_language_code(endpoint, values):
    # Check if "lang_code" is already in the URL values or if g.lang_code is  set.
    if "lang_code" in values or not g.lang_code:
        return  # Do nothing if lang_code is already in values or g.lang_code is  set.

    # Check if the endpoint expects a "lang_code" parameter.
    if app.url_map.is_endpoint_expecting(endpoint, "lang_code"):
        # Set the "lang_code" value in the values dictionary to g.lang_code.
        values["lang_code"] = g.lang_code


# Callback function for URL value preprocessors for all view functions of the application.
@app.url_value_preprocessor
def pull_lang_code(endpoint, values):
    # Pop the "lang_code" value from values dictionary and store it in g.lang_code.
    g.lang_code = values.pop("lang_code", None)


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
