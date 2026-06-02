from flask import Flask, render_template, request, redirect, session, flash
import sqlite3
import os

app = Flask(__name__,
            template_folder="templates",
            static_folder="static")

app.secret_key = "my_secret_key_123"

# Create folders
os.makedirs("static/images", exist_ok=True)
os.makedirs("static/css", exist_ok=True)

# Database Connection
def connect_db():

    conn = psycopg2.connect(

        host="dpg-d8f8pac2m8qs73e061og-a",

        database="ngo_db_p5gm",

        user="ngo_user",

        password="3TgPqG9heJ8eax5lkGBKyzNsOS9xfGdW",

        port="5432",

        sslmode="require"
    )

    return conn


# Create Slider Table
def create_slider_table():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS slider(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image TEXT
    )
    """)

    conn.commit()
    conn.close()

# Create Users Table
def create_users_table():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        email TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()

# Create tables when app starts
create_slider_table()
create_users_table()

# Home Page
@app.route("/")
def index():

    conn = connect_db()
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM slider")
        sliders = cur.fetchall()
    except:
        sliders = []

    conn.close()

    return render_template("index.html", sliders=sliders)

# About
@app.route("/about")
def about():
    return render_template("about.html")

# Gallery
@app.route("/gallery")
def gallery():
    return render_template("gallery.html")

# Donate
@app.route("/donate")
def donate():
    return render_template("donate.html")

# Register
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        conn = connect_db()
        cur = conn.cursor()

        try:
            cur.execute(
                "INSERT INTO users(username,email,password) VALUES(?,?,?)",
                (username, email, password)
            )
            conn.commit()
            flash("Registration Successful!")

        except:
            flash("Email already exists!")

        conn.close()

        return redirect("/login")

    return render_template("register.html")

# Login
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = connect_db()
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        )

        user = cur.fetchone()

        conn.close()

        if user:
            session["admin"] = email
            return redirect("/dashboard")

        flash("Invalid Email or Password")
        return redirect("/login")

    return render_template("login.html")

# Dashboard
@app.route("/dashboard")
def dashboard():

    if "admin" not in session:
        return redirect("/login")

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT id, username, email FROM users")
    users = cur.fetchall()

    conn.close()

    return render_template(
        "dash.html",
        users=users,
        email=session["admin"]
    )

# Show Users
@app.route("/users")
def users():

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT id, username, email FROM users")
    data = cur.fetchall()

    conn.close()

    return str(data)

# Logout
@app.route("/logout")
def logout():

    session.pop("admin", None)

    return redirect("/login")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

# Run App
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
