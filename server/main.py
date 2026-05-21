from flask import Flask, redirect, url_for, session, request, render_template 
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
app.secret_key = os.environ.get("APP_SECRET_KEY")
app.debug = True
AUTH0_BASE_URL= os.environ.get("AUTH0_DOMAIN")

auth0 = oauth.register(
    "auth0",
    auth_name = "request",
    client_id = os.environ.get("AUTH0_CLIENT_ID"),
    client_secret = os.environ.get("AUTH0_CLIENT_SECRET"),
    api_base_url = "http://127.0.0.1:5000/",
    client_kwargs = {"scope": "openid profile email" },
    server_metadata_url = f"https://{os.getenv('AUTH0_DOMAIN')}/.well-known/openid-configuration"
)

app.config["SESSION_TYPE"] = "filesystem"

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code



# ======================================== 
# ======== 🔐 Auth Routes ================ 
# ======================================== 
# login - send to Auth0
@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri="http://127.0.0.1:5000/callback"
    )
# callback - sends user data
@app.route("/callback")
def callback():
    # get token
    token = oauth.auth0.authorize_access_token()
    # get JSON payload
    user_info = token.get("userinfo")
    # extract & store user data in session
    session["user"] = user_info
    session["nickname"] = user_info["nickname"]
    session["picture"] = user_info["picture"]

    return redirect("/settings")

# logout - clear session
@app.route("/logout")
def logout():
    session.clear()

    return redirect("/")


# ======================================== 
# ======== 🔎 View Page Routes =========== 
# ======================================== 
@app.route("/")
def home():
    return render_template(
        "index.html"
    )

@app.route("/about")
def about():
    return "<h1>About Page</h1>"

@app.route("/api")
def api():
    return jsonify({
        "message": "Hello",
        "status": "working"
    })


# ======================================== 
# ==== 🛑 Settings/Protected Routes ====== 
# ======================================== 
@app.route("/settings")
def settings():

    user = session.get("user")

    if not user:
        return redirect("/")

    return render_template(
        "settings.html",
        user=user
    )

# ======== run app ========
if __name__ == "__main__":
    app.run(debug=True)

