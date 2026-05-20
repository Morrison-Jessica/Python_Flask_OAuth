from flask import Flask, redirect, url_for, session, request 
from flask import jsonify
import json 
from datetime import timedelta
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv, find_dotenv
from functools import wraps
import os


app = Flask(__name__)

oauth = OAuth(app)
app.secret_key = os.environ.get("AUTH0_SECRET")
app.debug = True
AUTH0_BASE_URL= os.environ.get("AUTH0_DOMAIN")

auth0 = oauth.register(
    "auth0",
    auth_name = "request",
    client_id = os.environ.get("AUTH0_CLIENT_ID"),
    client_secret = os.environ.get("AUTH0_CLIENT_SECRET"),
    api_base_url = "http://localhost:5000/",
    access_token_url = "",
    authorize_url = "",
    client_kwargs = {"scope": "openid profile email" },
    server_metadata_url = ""
)

app.config["SESSION_TYPE"] = "filesystem"

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


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

