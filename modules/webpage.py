from flask import Flask
from flask import redirect, url_for, abort, request
from flask import render_template, make_response

import time

app = Flask(__name__)


@app.route("/")
def blank():
    return redirect(url_for('home'))


@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/animation")
def animation():
    return render_template("anim.html")


@app.route("/whois/<name>")
@app.route("/whois/")
def who(name=None):
    if name:
        if name.lower() == "greg":
            text = "Greg is author of this page"
        else:
            text = f"I do not know {name}"
    else:
        text = "Is this a person?"
    return text


@app.route("/args/")
@app.route("/args/<name>")
def args(name=None):
    if not name:
        temp = request.args.get("name")
        if temp:
            name = temp
        else:
            name = "No name was provided."
    return name


@app.route("/picture", methods=["GET", "POST"])
def picture():
    if request.method == "GET":
        return "Getting image\n"
    else:
        return "None\n"


@app.route("/error")
def error():
    abort(405)


@app.errorhandler(404)
def error_handler(error):
    return render_template("missing.html"), 404


#
# @app.route("/results")
# def results():
#     cook = request.cookies.get("name")
#     cook = str(cook)
#     render = render_template("render.html", content=cook)
#     return render


@app.route("/save")
def save():
    render = render_template("main.html")
    resp = make_response(render)
    resp.set_cookie("name", "greg")
    return resp


@app.route("/about")
def about():
    render = render_template("render.html", content="This is me.")
    return render


if __name__ == "__main__":
    app.run(debug=True)
