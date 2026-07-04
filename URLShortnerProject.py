from flask import Flask, request, redirect, jsonify
import json
import os
import random
import string

app = Flask(__name__)
DATA_FILE = "url_store.json"
urls = {}


def load_store():
    global urls
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try:
                urls = json.load(f)
            except json.JSONDecodeError:
                urls = {}
    else:
        urls = {}


def save_store():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(urls, f, indent=2)


def generate_key(length=6):
    alphabet = string.ascii_letters + string.digits
    while True:
        key = ''.join(random.choice(alphabet) for _ in range(length))
        if key not in urls:
            return key


@app.route("/shorten", methods=["POST"])
def shorten_url():
    data = request.get_json(force=True)
    original_url = data.get("url")
    if not original_url:
        return jsonify({"error": "Missing url field"}), 400

    for code, target in urls.items():
        if target == original_url:
            return jsonify({"short_url": request.host_url + code})

    code = generate_key()
    urls[code] = original_url
    save_store()
    return jsonify({"short_url": request.host_url + code})


@app.route("/<code>")
def redirect_to_original(code):
    original_url = urls.get(code)
    if original_url:
        return redirect(original_url)
    return jsonify({"error": "Short URL not found"}), 404


@app.route("/stats", methods=["GET"])
def stats():
    return jsonify({"count": len(urls), "urls": urls})


@app.route("/", methods=["GET"])
def home():
    return """
    <!doctype html>
    <html lang=\"en\">
      <head>
        <meta charset=\"utf-8\">
        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
        <title>URL Shortener</title>
      </head>
      <body>
        <h1>URL Shortener</h1>
        <form id=\"shorten-form\">
          <label for=\"url-input\">Enter URL:</label><br>
          <input id=\"url-input\" name=\"url\" type=\"text\" size=\"50\" placeholder=\"https://example.com\" required><br><br>
          <button type=\"submit\">Shorten</button>
        </form>
        <p id=\"result\"></p>
        <script>
          const form = document.getElementById('shorten-form');
          const result = document.getElementById('result');

          form.addEventListener('submit', async (event) => {
            event.preventDefault();
            const url = document.getElementById('url-input').value;
            try {
              const response = await fetch('/shorten', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url })
              });
              const data = await response.json();
              if (response.ok) {
                result.innerHTML = `Short URL: <a href=\"${data.short_url}\">${data.short_url}</a>`;
              } else {
                result.textContent = data.error || 'An error occurred';
              }
            } catch (err) {
              result.textContent = 'Request failed: ' + err.message;
            }
          });
        </script>
      </body>
    </html>
    """


if __name__ == "__main__":
    load_store()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
