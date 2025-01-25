from sanic import Sanic, response
from sanic.response import html, redirect
from sanic_session import Session, InMemorySessionInterface
from sanic.log import logger
from sanic.response import text
from jinja2 import Environment, FileSystemLoader, select_autoescape
from dotenv import load_dotenv

import os, psycopg

import db_adapter

# Load environment variables
load_dotenv("../.env")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

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
async def setup_db(app, loop):
    app.ctx.db_adapter = db_adapter.DBAdapter(DB_CONFIG, logger)
    await app.ctx.db_adapter.connect()
    await app.ctx.db_adapter.init()

@app.listener('after_server_stop')
async def close_db(app, loop):
    await app.ctx.db_adapter.close()

# Helper function for rendering templates
def render_template(template_name, **context):
    template = env.get_template(template_name)
    return html(template.render(context))

@app.route("/", methods=["GET"])
async def index(request):
    if request.ctx.session.get("user"):
        return redirect("/dashboard")
    return render_template("login.html")

@app.route("/login", methods=["POST"])
async def login(request):
    username = request.form.get("username")
    password = request.form.get("password")

    async with app.ctx.db_pool.acquire() as conn:
        user = await conn.fetchrow(
            "SELECT * FROM users WHERE username = $1 AND password = $2", username, password
        )

    if user:
        request.ctx.session["user"] = dict(user)
        return redirect("/dashboard")

    return render_template("login.html", error="Invalid username or password")

@app.route("/dashboard", methods=["GET"])
async def dashboard(request):
    if not request.ctx.session.get("user"):
        return redirect("/")

    user = request.ctx.session["user"]
    return render_template("dashboard.html", user=user)

@app.route("/logout", methods=["GET"])
async def logout(request):
    request.ctx.session.clear()
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
