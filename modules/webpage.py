from flask import Flask
from flask import redirect, url_for, abort, request
from flask import render_template

app = Flask(__name__)


@app.route("/")
def blank():
    return redirect(url_for('home'))


@app.route("/home")
def home():
    return render_template("home.html")


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
    print(error)
    return render_template("missing.html"), 404


if __name__ == "__main__":
    app.run()
