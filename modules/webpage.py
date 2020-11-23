from flask import Flask
from flask import redirect, url_for, abort, request
from flask import render_template, make_response

# from flask_scss import Scss

import numpy as np
import time
import cv2
import os

app = Flask(__name__)

app.config["IMAGE_DIRECTORY"] = os.path.abspath("incoming")
os.makedirs(app.config['IMAGE_DIRECTORY'], exist_ok=True)

app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]


# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
# Scss(app)


@app.route("/")
def blank():
    return redirect(url_for('home'))


@app.route("/home/")
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


# @app.route("/favicon.ico")
# def favicon():
#     return None  # url_for("static", filename="favicon.ico")


@app.errorhandler(404)
def error_handler(error):
    return render_template("missing.html"), 404


@app.route("/upload", methods=["GET"])
def upload():
    render = render_template("upload.html")
    return render


@app.route("/process_image", methods=["GET", "POST"])
def process_image():
    if request.method == "GET":
        ret = redirect(url_for("upload"))
    elif request.method == "POST":
        ret = _save_image()
    else:
        ret = redirect(url_for("upload"))
    return ret


def _save_image():
    image = request.files["upImage"]
    try:
        name, extension = str(image.filename).split(".")
        if extension not in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
            return render_template("upload.html", header_text="Invalid format, try again.")
        else:
            print("valid")

    except Exception:
        abort(400)

    image.save(os.path.join(app.config["IMAGE_DIRECTORY"], str(int(time.time() * 100)) + f".{extension}"))


@app.route("/about")
def about():
    render = render_template("render.html", content="This is me.")
    return render


if __name__ == "__main__":
    app.run(debug=True)
