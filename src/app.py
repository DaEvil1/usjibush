from sanic import Sanic, response
from sanic.response import html, redirect
from sanic.request import Request
from sanic_session import Session, InMemorySessionInterface
from sanic.log import logger
from sanic.response import text
from jinja2 import Environment, FileSystemLoader, select_autoescape
from dotenv import load_dotenv

import os, psycopg, asyncio

import db_adapter, util, sessions

# Load environment variables
load_dotenv("../.env")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
SITE_URL = os.getenv("SITE_URL")

# Initialize the app and other components
app = Sanic("LoginApp")
session = Session(app, interface=InMemorySessionInterface())

# Set up Jinja2 environment for templates
env = Environment(
    loader=FileSystemLoader(os.getcwd() +'/src/templates'),
    autoescape=select_autoescape()
)

# Database credentials
DB_CONFIG = {
    "user": DB_USER,
    "password": DB_PASSWORD,
    "database": DB_NAME,
    "host": DB_HOST,
    "port": DB_PORT
}

@app.listener('before_server_start')
async def setup_db(app: Sanic, loop: asyncio.AbstractEventLoop):
    app.ctx.db_adapter = db_adapter.DBAdapter(DB_CONFIG, logger)
    await app.ctx.db_adapter.connect()
    await app.ctx.db_adapter.init()
    app.ctx.sessions = sessions.Sessions()
    app.ctx.util = util.Util(app.ctx.db_adapter)

@app.listener('after_server_stop')
async def close_db(app: Sanic, loop: asyncio.AbstractEventLoop):
    await app.ctx.db_adapter.close()

# Helper function for rendering templates
def render_template(template_name: str, **context: dict):
    template = env.get_template(template_name)
    return html(template.render(context))

@app.route("/style.css", methods=["GET"])
async def style(request: Request):
    return await response.file(os.getcwd() + "/src/templates/style.css")

@app.route("/", methods=["GET"])
async def index(request: Request):
    if request.cookies.get("session_token") in app.ctx.sessions.sessions:
        return redirect("/dashboard")
    return render_template("login.jinja")

@app.route("/login", methods=["POST"])
async def login(request: Request):
    username = request.form.get("username")
    password = request.form.get("password")

    logInObject = await request.app.ctx.util.login(username, password)
    if logInObject["success"]:
        sessionToken: str = await request.app.ctx.util.generate_session_token(username)
        await app.ctx.sessions.login(username, sessionToken)
        loginResponse = redirect("/dashboard")
        loginResponse.add_cookie("session_token", sessionToken)
        return loginResponse
    else:
        return render_template("login.jinja", error="Invalid credentials")

@app.route("/dashboard", methods=["GET"])
async def dashboard(request: Request):
    session_token = request.cookies.get("session_token")
    if not session_token or session_token not in app.ctx.sessions.sessions:
        return redirect("/")

    user: dict = app.ctx.sessions.sessions[session_token]
    return render_template("dashboard.jinja", user=user)

@app.route("/deadpool", methods=["GET"])
async def deadpool(request: Request):
    session_token = request.cookies.get("session_token")
    if not session_token or session_token not in app.ctx.sessions.sessions:
        return redirect("/")
    user: dict = app.ctx.sessions.sessions[session_token]
    return render_template("deadpool.jinja", user=user)

@app.route("/review_burger", methods=["GET"])
async def review_burger(request: Request):
    session_token = request.cookies.get("session_token")
    if not session_token or session_token not in app.ctx.sessions.sessions:
        return redirect("/")
    user: dict = app.ctx.sessions.sessions[session_token]
    return render_template("review_burger.jinja", user=user)

@app.route("/burger_reviews", methods=["GET"])
async def burger_reviews(request: Request):
    session_token = request.cookies.get("session_token")
    if not session_token or session_token not in app.ctx.sessions.sessions:
        return redirect("/")
    user: dict = app.ctx.sessions.sessions[session_token]
    return render_template("burger_reviews.jinja", user=user)

@app.route("/burger_review/<id>", methods=["GET"])
async def burger_review(request: Request, id: str):
    session_token = request.cookies.get("session_token")
    if not session_token or session_token not in app.ctx.sessions.sessions:
        return redirect("/")
    user: dict = app.ctx.sessions.sessions[session_token]
    return render_template("burger_review.jinja", user=user)

@app.route("/logout", methods=["GET"])
async def logout(request: Request):
    request.ctx.session.clear()
    session_token = request.cookies.get("session_token")
    if session_token:
        await app.ctx.sessions.logout(session_token)
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

# Directory structure:
# .
# ├── app.py
# └── templates
#     ├── login.html
#     └── dashboard.html

# Example templates:
# login.html:
# <html>
# <head><title>Login</title></head>
# <body>
#   <h1>Login</h1>
#   <form method="POST" action="/login">
#     <input type="text" name="username" placeholder="Username" required />
#     <input type="password" name="password" placeholder="Password" required />
#     <button type="submit">Login</button>
#   </form>
#   {% if error %}
#     <p style="color: red;">{{ error }}</p>
#   {% endif %}
# </body>
# </html>

# dashboard.html:
# <html>
# <head><title>Dashboard</title></head>
# <body>
#   <h1>Welcome, {{ user.username }}</h1>
#   <a href="/logout">Logout</a>
# </body>
# </html>
