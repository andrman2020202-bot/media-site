from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secretkey123"

def db():
    return sqlite3.connect("database.db")

# база
conn = db()
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
""")
conn.commit()
conn.close()

# регистрация
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        conn = db()
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (u, p))
        conn.commit()
        conn.close()

        session["user"] = u
        session["pass"] = p

        return redirect("/profile")

    return render_template("register.html")

# логин
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        conn = db()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (u, p))
        user = c.fetchone()
        conn.close()

        if user:
            session["user"] = u
            session["pass"] = p
            return redirect("/home")

    return render_template("login.html")

# главное меню
@app.route("/home")
def home():
    if "user" not in session:
        return redirect("/login")

    return render_template("home.html", user=session["user"])

# кабинет
@app.route("/profile")
def profile():
    if "user" not in session:
        return redirect("/login")

    return render_template(
        "profile.html",
        user=session["user"],
        password=session["pass"]
    )

if __name__ == "__main__":
    app.run(debug=True)