from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3
import os

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)
app.secret_key = "pongston_secret"

app = Flask(__name__)
app.secret_key = "pongston_secret"

def db():
    return sqlite3.connect("database.db")

# สร้างตาราง
with db() as con:
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        password TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY,
        customer TEXT,
        site TEXT,
        agency TEXT
    )
    """)
    cur.execute("INSERT OR IGNORE INTO users VALUES (1,'admin','1234')")
    con.commit()

@app.route("/", methods=["GET"])
def home():
    if "user" not in session:
        return redirect("/login")
    return render_template("index.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]
        cur = db().cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (u,p))
        if cur.fetchone():
            session["user"] = u
            return redirect("/")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/data")
def data():
    cur = db().cursor()
    cur.execute("SELECT * FROM customers")
    rows = cur.fetchall()
    return jsonify([
        {"id":r[0],"customer":r[1],"site":r[2],"agency":r[3]} for r in rows
    ])

@app.route("/add", methods=["POST"])
def add():
    d = request.json
    with db() as con:
        con.execute(
            "INSERT INTO customers (customer,site,agency) VALUES (?,?,?)",
            (d["customer"],d["site"],d["agency"])
        )
        con.commit()
    return "ok"

@app.route("/delete/<id>", methods=["DELETE"])
def delete(id):
    with db() as con:
        con.execute("DELETE FROM customers WHERE id=?", (id,))
        con.commit()
    return "ok"

if __name__ == "__main__":
    app.run()