from functools import wraps

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import Flask
from flask import redirect, url_for, abort, request
from flask import render_template, make_response
# from flask_scss import Scss

from backend.tasks import create_zoomgif, create_mozaic
from backend.celery import app as celery_app

import logging
import numpy as np
import hashlib
import pickle
import time
import cv2
import os

app = Flask(__name__)
limiter = Limiter(
        default_limits=["30/minute"],
        key_func=get_remote_address)
limiter.init_app(app)

logger = logging.getLogger("flask")
logger.setLevel("INFO")

counter = logging.getLogger("count_endpoints")
counter.setLevel("INFO")

fh = logging.FileHandler("flask.log", mode='a')
fh_counter = logging.FileHandler("count.log", mode='a')
ch = logging.StreamHandler()

formatter = logging.Formatter(f"%(asctime)s - %(name)s - %(levelname)s - %(message)s")
formatter_count = logging.Formatter(f"%(asctime)s - %(message)s")

fh.setFormatter(formatter)
ch.setFormatter(formatter)
fh_counter.setFormatter(formatter_count)

logger.addHandler(fh)
logger.addHandler(ch)
counter.addHandler(fh_counter)

app.logger = logger
app.counter = counter

app.config["IMAGE_DIRECTORY"] = os.path.abspath("incoming")
app.config["RESOURCE_DIR_NAME"] = "outputpics"
app.config["RESOURCE_DIRECTORY"] = os.path.abspath(os.path.join("static", app.config["RESOURCE_DIR_NAME"]))

os.makedirs(app.config['IMAGE_DIRECTORY'], exist_ok=True)
os.makedirs(app.config['RESOURCE_DIRECTORY'], exist_ok=True)

app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["jpeg", "jpg", "png"]

"===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== "


# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
# Scss(app)

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


def log_endpoint(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        req = request
        app.counter.info(req.url_rule)
        app.logger.info(f"{req.method}: {req.path}")
        return f(*args, **kwargs)

    return wrapper


@app.route("/")
@log_endpoint
def blank():
    return redirect(url_for('home'))


@app.route("/home/")
@log_endpoint
def home():
    return render_template("home.html")


@app.route("/animation/")
@log_endpoint
def animation():
    return render_template("anim.html")


@app.route("/clocks/")
@limiter.exempt
@app.errorhandler(429)
@log_endpoint
def clocks(er=None):
    was_uploading = r"process_image" in request.endpoint
    if er:
        return render_template("clocks.html", rate_error=er, hide_navbar=not was_uploading)
    return render_template("clocks.html")


@app.errorhandler(404)
@app.errorhandler(400)
@log_endpoint
def error_handler(error):
    app.logger.error(f"{error.code}: {error}")
    errorCode = error.code
    return render_template("error.html", error=error, errorCode=errorCode), errorCode


@app.route("/newgif", methods=["GET"])
@log_endpoint
def new_gif():
    render = render_template("upload_gif_form.html")
    return render


@app.route("/process_image", methods=["GET", "POST"])
@limit_content_length(5 * 1024 * 1024)
@limiter.limit("10/1hour")
@log_endpoint
def validate_image():
    if request.method == "GET":
        ret = redirect(url_for("new_gif"))
    elif request.method == "POST":
        ret = _validate()
    else:
        ret = redirect(url_for("new_gif"))
    return ret


def _validate():
    enter = f"{np.random.random(100)}"
    secr = f"{enter}-{time.time()}".encode()
    ah = hashlib.sha1(secr)
    new_token = ah.hexdigest()
    jobtoken = f"{int(time.time())}-{new_token}"

    valid = _save_image(jobtoken)
    if valid:
        power = request.form.get("powerBar", 50)
        outsize = request.form.get("sizeBar", 200)
        palette = request.form.get("palette", None)
        mode = request.form.get("mode", 0)

        power = int(power)
        outsize = int(outsize)
        mode = int(mode)

        if palette:
            palette = [str(palette)]

        if power < 10 or power > 150:
            abort(400)

        if mode == 0:
            "Check params for mozaic"

            make_bigger = request.form.get("makeBigger", False)
            if power < 10 or power > 150:
                abort(400)

            if make_bigger:
                pic_format = "jpg"
                outsize *= 2
            else:
                pic_format = "png"

            if not make_bigger and (outsize < 50 or outsize > 1000):
                abort(400)

            if make_bigger and (outsize < 50 or outsize > 2000):
                abort(400)

            res = create_mozaic.delay(jobtoken, power, pic_format, outsize, palette=palette)
            jobid = res.id

        elif mode == 1:
            "Check params for zoom"
            pic_format = "gif"
            if outsize < 50 or outsize > 400:
                abort(400)
            res = create_zoomgif.delay(jobtoken, power, outsize, palette=palette)
            jobid = res.id
        else:
            abort(400)

        app.logger.info(f"Accepted job: pow:{power} outsize:{outsize} palette:{palette}")
        destination = url_for("showresult", token=jobtoken, jobid=jobid, format=pic_format)
        response = make_response(render_template("process.html", destination=destination))

    else:
        app.logger.error("Picture is not valid")
        response = make_response(render_template("process.html"))

    return response


def _save_image(dest_name):
    image = request.files["upImage"]
    imbytes = request.files['upImage'].read()
    # bytesLike = BytesIO(imstr)

    try:
        npimg = np.frombuffer(imbytes, np.uint8)
        npimg = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        *name, extension = str(image.filename).split(".")
        # print(f"name: {name}, extension: {extension}")
        outname = f"{dest_name}.png"
        outpath = os.path.join(app.config['IMAGE_DIRECTORY'], outname)

        if extension.lower() not in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
            return False
        app.logger.info(f"saving image: {outname}")
        cv2.imwrite(outpath, npimg)
        return True

    except Exception as err:
        app.logger.error(f"Error when saving image: {err}")
        return False


@app.route("/result/<format>/<token>/<jobid>/", methods=["GET"])
@app.route("/result/<format>/<token>/", methods=["GET"])
@app.route("/result/")
@limiter.exempt
@log_endpoint
def showresult(format=None, token=None, jobid=None):
    fileFormat = str(format) if format else "gif"
    fileFormat = fileFormat.lower()

    imgPath = os.path.join(app.config['RESOURCE_DIRECTORY'], f"{token}.{fileFormat}")
    isImage = os.path.isfile(imgPath)
    avg_time = 1

    url = url_for("static", filename=f"{app.config['RESOURCE_DIR_NAME']}/{token}.{fileFormat}")
    if isImage:
        app.logger.info(f"Sending image, size: {os.stat(imgPath).st_size / 1000:4.1f}kB")
        return render_template("process_results.html", imgPath=url)
    elif jobid:
        try:
            isProc, isQue, quePos = find_job_in_celery(jobid)
            if isProc:
                text = "Your image is now generated."
            elif isQue:
                text = f"Your image is in queue, position: {quePos}. Max time est: {quePos * avg_time} min"
            elif quePos >= 9:
                text = f"Your image is in queue, position: 10+"
            else:
                text = "Image is missing. Is this valid request?"
        except Exception as err:
            app.logger.error(f"Checking que error: {err}")
            text = "Error when checking que."

        return render_template("process_results.html", workStatus=text)
    else:
        abort(400)


# @app.route("/jpg/<token>/<jobid>", methods=["GET"])
# @app.route("/jpg/<token>/", methods=["GET"])
# @limiter.exempt
# @log_endpoint
# def jpg(token=None, jobid=None):
#     imgPath = os.path.join(app.config['RESOURCE_DIRECTORY'], f"{token}.jpg")
#     isImage = os.path.isfile(imgPath)
#     avg_time = 1
#
#     url = url_for("static", filename=f"{app.config['RESOURCE_DIR_NAME']}/{token}.jpg")
#     if isImage:
#         app.logger.info(f"Sending image, size: {os.stat(imgPath).st_size / 1000:4.1f}kB")
#         return render_template("process_results.html", imgPath=url)
#     elif jobid:
#         try:
#             isProc, isQue, quePos = find_job_in_celery(jobid)
#             if isProc:
#                 text = "Your image is now generated."
#             elif isQue:
#                 text = f"Your image is in queue, position: {quePos}. Max time est: {quePos * avg_time} min"
#             elif quePos >= 9:
#                 text = f"Your image is in queue, position: 10+"
#             else:
#                 text = "Image is missing. Is this valid request?"
#         except Exception as err:
#             app.logger.error(f"Checking que error: {err}")
#             text = "Error when checking que."
#
#         return render_template("process_results.html", workStatus=text)
#     else:
#         abort(400)

# @app.route("/png/<token>/<jobid>", methods=["GET"])
# @app.route("/png/<token>/", methods=["GET"])
# @limiter.exempt
# @log_endpoint
# def png(token=None, jobid=None):
#     imgPath = os.path.join(app.config['RESOURCE_DIRECTORY'], f"{token}.jpg")
#     isImage = os.path.isfile(imgPath)
#     avg_time = 1
#
#     url = url_for("static", filename=f"{app.config['RESOURCE_DIR_NAME']}/{token}.jpg")
#     if isImage:
#         app.logger.info(f"Sending image, size: {os.stat(imgPath).st_size / 1000:4.1f}kB")
#         return render_template("process_results.html", imgPath=url)
#     elif jobid:
#         try:
#             isProc, isQue, quePos = find_job_in_celery(jobid)
#             if isProc:
#                 text = "Your image is now generated."
#             elif isQue:
#                 text = f"Your image is in queue, position: {quePos}. Max time est: {quePos * avg_time} min"
#             elif quePos >= 9:
#                 text = f"Your image is in queue, position: 10+"
#             else:
#                 text = "Image is missing. Is this valid request?"
#         except Exception as err:
#             app.logger.error(f"Checking que error: {err}")
#             text = "Error when checking que."
#
#         return render_template("process_results.html", workStatus=text)
#     else:
#         abort(400)
#

def find_job_in_celery(jobid):
    i = celery_app.control.inspect()
    reg = list(i.registered().keys())[0]
    i = celery_app.control.inspect([reg])

    queue = 0
    is_processed = False
    is_inQueue = False

    # # print(f"Celery name: {dir(celery_app)}")
    # # print(f"Celery name: {dir(celery_app.WorkController)}")
    # # print(f"Celery name: {celery_app.WorkController}")
    # query = i.query_task(jobid)
    # actq = i.active_queues()
    # # reg = i.registered()
    # # regtk = i.registered_tasks()
    # print(f"\n {'==' * 30}" * 3)
    # print(f"query: {query}")
    # print(f"actqu: {actq}")
    # # print(f"reg: {reg}")
    # # print(f"regtk: {regtk}")

    act = i.active()
    try:
        # print(f"que1: {len(act)}")
        for key, val in act.items():
            if is_processed:
                break
            for worker in val:
                this_id = worker['id']
                if this_id == jobid:
                    is_processed = True
                    break
    except Exception as err:
        print(f"JOB FIND ERROR1: {err}")
        is_processed = False

    try:
        que = i.reserved()
        # print(f"que2: {len(que)}")
        if not is_processed:
            if que:
                for key, job_list in que.items():
                    if is_inQueue:
                        break
                    for job in job_list:
                        queue += 1
                        this_id = job['id']
                        if this_id == jobid:
                            is_inQueue = True
                            break
    except Exception as err:
        print(f"JOB FIND ERROR2: {err}")
    # try:
    #     sch = i.scheduled()
    #     if not (is_processed or is_inQueue):
    #         if sch:
    #             print(f"que3: {len(sch)}")
    #             for key, val in sch.items():
    #                 queue += 1
    #                 this_id = val[0]['id']
    #                 if this_id == jobid:
    #                     is_inQueue = True
    #                     break
    # except Exception as err:
    #     print(f"JOB FIND ERROR3: {err}")

    # print("act:", act)
    # print("que:", que)
    # print("sch:", sch)
    print(f"PRoc: {is_processed}, isque: {is_inQueue}, que: {queue}")
    return is_processed, is_inQueue, queue


@app.route("/about")
@log_endpoint
def about():
    render = render_template("about.html")
    return render


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
