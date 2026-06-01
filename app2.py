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
    return sqlite3.connect("slider.db")

# Create Users Table
def create_table():
    conn = sqlite3.connect("slider.db")
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
# Home Page
@app.route("/")
def index():

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM slider")
    sliders = cur.fetchall()

    conn.close()

    return render_template("index.html", sliders=sliders)

# About Page
@app.route("/about")
def about():
    return render_template("about.html")

# Gallery Page
@app.route("/gallery")
def gallery():
    return render_template("gallery.html")

@app.route("/donate")
def donate():
    return render_template("donate.html")

# Register Page
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        conn = connect_db()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO users(username,email,password) VALUES(?,?,?)",
            (username, email, password)
        )

        conn.commit()
        conn.close()

        flash("✅ Registration Successful!")

        return redirect("/login")

    return render_template("register.html")
# Login Page
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

            flash("✅ Login Successful!")

            return redirect("/dashboard")

        else:

            flash("❌ Invalid Email or Password!")

            return redirect("/login")

    return render_template("login.html")

# Dashboard Page
@app.route("/dashboard")
def dashboard():

    if "admin" not in session:
        return redirect("/login")

    return render_template(
        "dash.html",
        name=session["admin"]
    )

# Delete Slider
@app.route("/delete/<int:id>")
def delete(id):

    conn = connect_db()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM slider WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    flash("🗑️ Image Deleted Successfully!")

    return redirect("/dashboard")

# Logout
@app.route("/logout")
def logout():

    session.pop("admin", None)

    flash("✅ Logged Out Successfully!")

    return redirect("/login")


# Run App
if __name__ == "__main__":
    app.run(debug=True)
