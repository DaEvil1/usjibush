from sanic import Sanic, response
from sanic.response import html, redirect
from sanic.request import Request
from sanic_session import Session, InMemorySessionInterface
from sanic.log import logger
from sanic.response import text
from jinja2 import Environment, FileSystemLoader, select_autoescape
from dotenv import load_dotenv

import os, psycopg, asyncio, datetime

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
app = Sanic("Usjibush")
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

@app.route("/", methods=["GET"])
async def index(request: Request):
    if request.cookies.get("session_token") in app.ctx.sessions.sessions:
        return redirect("/profile")
    return render_template("login.jinja")

@app.route("/login", methods=["POST"])
async def login(request: Request):
    username = request.form.get("username")
    password = request.form.get("password")

    logInObject = await request.app.ctx.util.login(username, password)
    if logInObject["success"]:
        sessionToken: str = await request.app.ctx.util.generate_session_token(username)
        await app.ctx.sessions.login(username, sessionToken)
        loginResponse = redirect("/profile")
        loginResponse.add_cookie("session_token", sessionToken)
        return loginResponse
    else:
        return render_template("login.jinja", error="Invalid credentials")

@app.route("/profile", methods=["GET"])
async def profile(request: Request):
    session_token = request.cookies.get("session_token")
    if not session_token or session_token not in app.ctx.sessions.sessions:
        return redirect("/")

    user: dict = app.ctx.sessions.sessions[session_token]
    return render_template("profile.jinja", user=user)

@app.route("/deadpool", methods=["GET"])
async def deadpool(request: Request):
    session_token = request.cookies.get("session_token")
    if not session_token or session_token not in app.ctx.sessions.sessions:
        return redirect("/")
    user: dict = app.ctx.sessions.sessions[session_token]
    deadpool_results = await app.ctx.util.get_deadpool_results()
    current_guess = await app.ctx.util.get_deadpool_guess(user.username)
    is_admin = await app.ctx.util.is_admin(user.username)
    today = datetime.date.today()
    next_month = (today.replace(day=28) + datetime.timedelta(days=4)).strftime("%B")
    previous_month = (today.replace(day=1) - datetime.timedelta(days=1)).strftime("%B")
    result_previous_month = await app.ctx.util.get_deadpool_answer_previous_month()
    return render_template(
        "deadpool.jinja",
        user=user,
        is_admin=is_admin,
        deadpool_results=deadpool_results,
        current_guess=current_guess,
        next_month=next_month,
        previous_month=previous_month,
        result_previous_month=result_previous_month
        )

@app.route("/deadpool", methods=["POST"])
async def deadpool_post(request: Request):
    session_token = request.cookies.get("session_token")
    if not session_token or session_token not in app.ctx.sessions.sessions:
        return redirect("/")
    user: dict = app.ctx.sessions.sessions[session_token]
    amount = request.form.get("amount")
    await app.ctx.util.add_deadpool_guess(user.username, amount)
    return redirect("/deadpool")

@app.route("/deadpool_result", methods=["POST"])
async def deadpool_results_post(request: Request):
    session_token = request.cookies.get("session_token")
    if not session_token or session_token not in app.ctx.sessions.sessions:
        return redirect("/")
    user: dict = app.ctx.sessions.sessions[session_token]
    if not await app.ctx.util.is_admin(user.username):
        return redirect("/")
    amount = request.form.get("amount")
    await app.ctx.util.set_deadpool_answer_previous_month(amount)
    await app.ctx.util.set_deadpool_winners_previous_month()
    return redirect("/deadpool")

@app.route("/review_burger", methods=["GET"])
async def review_burger_get(request: Request):
    session_token = request.cookies.get("session_token")
    if not session_token or session_token not in app.ctx.sessions.sessions:
        return redirect("/")
    user: dict = app.ctx.sessions.sessions[session_token]
    burger_locations = await app.ctx.util.get_burger_locations()
    return render_template("review_burger.jinja", user=user, burger_locations=burger_locations)

@app.route("/review_burger", methods=["POST"])
async def review_burger_post(request: Request):
    session_token = request.cookies.get("session_token")
    if not session_token or session_token not in app.ctx.sessions.sessions:
        return redirect("/")

    user: dict = app.ctx.sessions.sessions[session_token]
    review: dict = {
        "location": request.form.get("location"),
        "date": request.form.get("date"),
        "burger_name": request.form.get("burger_name"),
        "bun_rating": request.form.get("bun_rating"),
        "bun_remarks": request.form.get("bun_remarks"),
        "patty_rating": request.form.get("patty_rating"),
        "patty_remarks": request.form.get("patty_remarks"),
        "toppings_rating": request.form.get("toppings_rating"),
        "toppings_remarks": request.form.get("toppings_remarks"),
        "fries_rating": request.form.get("fries_rating"),
        "fries_remarks": request.form.get("fries_remarks"),
        "location_rating": request.form.get("location_rating"),
        "location_remarks": request.form.get("location_remarks"),
        "value_rating": request.form.get("value_rating"),
        "value_remarks": request.form.get("value_remarks"),
        "x_factor_rating": request.form.get("x_factor_rating"),
        "x_factor_remarks": request.form.get("x_factor_remarks"),
    }
    await app.ctx.util.add_burger_review(user.username, review)
    return redirect("/burger_review_submitted")

@app.route("/burger_reviews", methods=["GET"])
async def burger_reviews(request: Request):
    session_token = request.cookies.get("session_token")
    if not session_token or session_token not in app.ctx.sessions.sessions:
        return redirect("/")
    user: dict = app.ctx.sessions.sessions[session_token]
    burger_reviews = await app.ctx.util.get_all_burger_reviews()
    return render_template("burger_reviews.jinja", user=user, burger_reviews=burger_reviews)

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

@app.route("/change_password", methods=["POST"])
async def change_password(request: Request):
    session_token = request.cookies.get("session_token")
    if not session_token or session_token not in app.ctx.sessions.sessions:
        return redirect("/")
    user: dict = app.ctx.sessions.sessions[session_token]
    current_password = request.form.get("current_password") if request.form.get("current_password") else ""
    new_password = request.form.get("new_password") if request.form.get("new_password") else ""
    confirm_new_password = request.form.get("confirm_new_password") if request.form.get("confirm_new_password") else ""
    if new_password != confirm_new_password:
        return render_template("profile.jinja", user=user, error="New passwords do not match")
    login: dict = await app.ctx.util.login(user.username, current_password)
    if not login["success"]:
        return render_template("profile.jinja", user=user, error="Incorrect password")
    await app.ctx.util.change_password(user.username, new_password)
    return render_template("profile.jinja", user=user, success="Password changed")

@app.route("/burger_review_submitted", methods=["GET"])
async def burger_review_submitted(request: Request):
    session_token = request.cookies.get("session_token")
    if not session_token or session_token not in app.ctx.sessions.sessions:
        return redirect("/")
    user: dict = app.ctx.sessions.sessions[session_token]
    return render_template("burger_review_submitted.jinja", user=user)

# static
app.static("/static", os.getcwd() + "/src/static")

# rest
@app.route("/rest/burger_review/<burger_location_id>", methods=["GET"])
async def rest_burger_review(request: Request, burger_location_id: str):
    session_token = request.cookies.get("session_token")
    if not session_token or session_token not in app.ctx.sessions.sessions:
        return response.json({"error": "Not logged in"}, status=401)
    user: dict = app.ctx.sessions.sessions[session_token]
    burger_review = await app.ctx.util.get_burger_reviews(user.username, burger_location_id)
    return response.json(burger_review, default=str)

@app.route("/rest/burger_locations", methods=["GET"])
async def rest_burger_locations(request: Request):
    burger_locations = await app.ctx.util.get_burger_locations()
    return response.json(burger_locations)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)