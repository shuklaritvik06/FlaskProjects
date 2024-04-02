from flask import Flask, jsonify, g
import aiohttp


app = Flask(__name__)


# Callback function for URL defaults for all view functions of the application.
@app.url_defaults
def add_language_code(endpoint, values):
    # Check if "lang_code" is already in the URL values or if g.lang_code is not  set.
    if "lang_code" in values or not g.lang_code:
        return  # Do nothing if lang_code is already in values or g.lang_code is not  set.

    # Check if the endpoint expects a "lang_code" parameter.
    if app.url_map.is_endpoint_expecting(endpoint, "lang_code"):
        # Set the "lang_code" value in the values dictionary to g.lang_code.
        values["lang_code"] = g.lang_code


# Callback function for URL value preprocessors for all view functions of the application.
@app.url_value_preprocessor
def pull_lang_code(endpoint, values):
    # Pop the "lang_code" value from values dictionary and store it in g.lang_code.
    if values is None:
        return
    g.lang_code = values.pop("lang_code", None)


async def fetch_data():
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://jsonplaceholder.typicode.com/todos"
        ) as response:
            return await response.json()


@app.route("/")
async def index():
    data = await fetch_data()
    return jsonify(data)


# Here there is no requirements for the path to be given as the function arguements
@app.route("/hello/<lang_code>")
async def handle_lang_code():
    return "Hello lang code"


@app.route("/hi/<ramesh>")
async def handle_ramesh(ramesh):
    return f"Hello {ramesh}"


if __name__ == "__main__":
    app.run(debug=True)
