from flask import Flask
from flask import jsonify
from datetime import timedelta
import json
from os import environ as env
from urllib.parse import quote_plus, urlencode
from dotenv import load_dotenv, find_dotenv
from functtools import wraps


app = Flask(__name__)

# ======================================== 
# ============== Route Func ================== 
# ======================================== 
@app.route("/")
def home():
    return "<h1>Home Page</h1>"

@app.route("/about")
def about():
    return "<h1>About Page</h1>"

@app.route("/api")
def api():
    return jsonify({
        "message": "Hello",
        "status": "working"
    })


# ======== run app ========
if __name__ == "__main__":
    app.run(debug=True)

