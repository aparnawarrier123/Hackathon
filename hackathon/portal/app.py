import sqlite3
from flask import Flask, jsonify, request, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "dev-secret-change-me"   # NEW: used to sign the session cookie


def get_db():
    conn = sqlite3.connect("portal.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            stored_path TEXT NOT NULL
        )
    """)
    db.commit()
    db.close()


@app.route("/hello")
def hello():
    return "Hello from our portal"


@app.route("/team")
def team():
    return "We are Team Commit and regret"


# NEW: learning-only route to see the users table (we delete it later)
@app.route("/users")
def list_users():
    rows = get_db().execute("SELECT id, username FROM users").fetchall()
    return jsonify([dict(r) for r in rows])


# NEW: register
@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    db = get_db()
    try:
        db.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, generate_password_hash(password)),
        )
        db.commit()
    except sqlite3.IntegrityError:          # username already exists
        return jsonify(error="username taken"), 400
    return jsonify(message="registered"), 201


# NEW: login
@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    user = get_db().execute(
        "SELECT * FROM users WHERE username = ?", (username,)
    ).fetchone()
    if user and check_password_hash(user["password_hash"], password):
        session["user_id"] = user["id"]     # put the wristband on
        return jsonify(message="logged in")
    return jsonify(error="bad credentials"), 401


# NEW: who am I? (to prove the session works)
@app.route("/me")
def me():
    if "user_id" not in session:
        return jsonify(error="login required"), 401
    return jsonify(user_id=session["user_id"])


init_db()
app.run(debug=True)