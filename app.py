from flask import Flask, render_template
import traceback

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

@app.route("/login")
def login():
    try:
        return render_template("login.html")
    except Exception as e:
        return "<pre>" + traceback.format_exc() + "</pre>", 500

@app.route("/")
def home():
    return "HOME OK"

if __name__ == "__main__":
    app.run()