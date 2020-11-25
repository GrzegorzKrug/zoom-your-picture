from functools import wraps

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import Flask
from flask import redirect, url_for, abort, request
from flask import render_template, make_response

# from flask_scss import Scss

import numpy as np
import time
import cv2
import os

app = Flask(__name__)
limiter = Limiter(
        default_limits=["30/minute"],
        key_func=get_remote_address)
limiter.init_app(app)

app.config["IMAGE_DIRECTORY"] = os.path.abspath("incoming")
os.makedirs(app.config['IMAGE_DIRECTORY'], exist_ok=True)

app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["jpeg", "jpg", "png"]

"===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== "


# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
# Scss(app)


@app.route("/")
def blank():
    return redirect(url_for('home'))


@app.route("/home/")
def home():
    return render_template("home.html")


@app.route("/animation/")
def animation():
    return render_template("anim.html")


@app.route("/clocks/")
@limiter.exempt
@app.errorhandler(429)
def clocks(er=None):
    was_uploading = r"process_image" in request.endpoint
    print(f"upload: {was_uploading}")
    if er:
        return render_template("clocks.html", rate_error=er, hide_navbar=not was_uploading)
    return render_template("clocks.html")


@app.errorhandler(404)
def error_handler(error):
    return render_template("missing.html"), 404


@app.route("/newgif", methods=["GET"])
def new_gif():
    render = render_template("upload_gif_form.html")
    return render


def limit_content_length(max_length):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            cl = request.content_length
            if cl is not None and cl > max_length:
                abort(413)
            return f(*args, **kwargs)

        return wrapper

    return decorator


@app.route("/process_image", methods=["GET", "POST"])
@limit_content_length(5 * 1024 * 1024)
@limiter.limit("3/5minute")
def process_image():
    print("Starting process")
    if request.method == "GET":
        ret = redirect(url_for("newGif"))
    elif request.method == "POST":
        try:
            ret = _save_image()
        except Exception:
            ret = redirect(url_for("newGif"))
    else:
        ret = redirect(url_for("newGif"))
    return ret


def _save_image():
    image = request.files["upImage"]
    try:
        name, extension = str(image.filename).split(".")
        print(f"name: {name}, extension: {extension}")
        if extension.lower() not in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
            return render_template("upload_gif_form.html", header_text="Invalid format, try again.")
        else:
            return render_template("process.html")
    except Exception:
        abort(400)

    # image.save(os.path.join(app.config["IMAGE_DIRECTORY"], str(int(time.time() * 100)) + f".{extension}"))


@app.route("/about")
def about():
    render = render_template("render.html", content="This is me.")
    return render


if __name__ == "__main__":
    app.run(debug=True)
