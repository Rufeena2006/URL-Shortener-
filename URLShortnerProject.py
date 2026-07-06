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
    return"""
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>URL Shortener</title>

    <style>
        *{
            margin:0;
            padding:0;
            box-sizing:border-box;
            font-family:Arial, Helvetica, sans-serif;
        }

        body{
            height:100vh;
            display:flex;
            justify-content:center;
            align-items:center;
            background:linear-gradient(135deg,#4facfe,#8e44ad);
        }

        .container{
            background:white;
            padding:40px;
            border-radius:15px;
            width:420px;
            text-align:center;
            box-shadow:0 10px 25px rgba(0,0,0,0.3);
        }

        h1{
            color:#4b0082;
            margin-bottom:15px;
        }

        p{
            color:#555;
            margin-bottom:20px;
        }

        input{
            width:100%;
            padding:12px;
            border:2px solid #4facfe;
            border-radius:8px;
            font-size:16px;
            outline:none;
            margin-bottom:20px;
        }

        input:focus{
            border-color:#8e44ad;
        }

        button{
            width:100%;
            padding:12px;
            background:linear-gradient(135deg,#4facfe,#8e44ad);
            color:white;
            border:none;
            border-radius:8px;
            font-size:17px;
            cursor:pointer;
            transition:0.3s;
        }

        button:hover{
            transform:scale(1.05);
            opacity:0.9;
        }

        #result{
            margin-top:20px;
            font-size:17px;
            font-weight:bold;
        }

        #result a{
            color:#0066cc;
            text-decoration:none;
        }

        #result a:hover{
            text-decoration:underline;
        }
    </style>
</head>

<body>

<div class="container">
    <h1>🔗 URL Shortener</h1>

    <p>Convert your long URLs into short and easy-to-share links.</p>

    <form id="shorten-form">
        <input
            id="url-input"
            type="text"
            placeholder="https://example.com"
            required
        >

        <button type="submit">Shorten URL</button>
    </form>

    <p id="result"></p>
</div>

<script>
const form = document.getElementById('shorten-form');
const result = document.getElementById('result');

form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const url = document.getElementById('url-input').value;

    try {
        const response = await fetch('/shorten', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url })
        });

        const data = await response.json();

        if (response.ok) {
            result.innerHTML = `
                ✅ Short URL:<br><br>
                <a href="${data.short_url}" target="_blank">
                    ${data.short_url}
                </a>
            `;
        } else {
            result.innerHTML = `<span style="color:red;">${data.error}</span>`;
        }

    } catch (err) {
        result.innerHTML = `<span style="color:red;">Request failed: ${err.message}</span>`;
    }
});
</script>

</body>
</html>"""

if __name__ == "__main__":
    load_store()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
