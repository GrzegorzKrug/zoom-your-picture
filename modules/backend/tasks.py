from .celery import app
from .create_gif import start_job_zoom, start_job_mozaic
from .logger_shared import logger

import time
import os


@app.task
def create_zoomgif(name: str, power: int, output_maxsize: int = None, palette=None):
    src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', "incoming", f"{name}.png"))
    out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', "static", "outputpics", f"{name}.gif"))
    try:
        start_job_zoom(src_path, out_path, power, output_maxsize, palette)
    except Exception as err:
        logger.error(f"Uncaught error during job: {err}")


@app.task
def create_mozaic(name: str, power: int, fileFormat: str, output_maxsize: int = None, palette=None):
    src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', "incoming", f"{name}.png"))
    out_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', "static", "outputpics", f"{name}.{fileFormat}"))
    try:
        start_job_mozaic(src_path, out_path, power, output_maxsize, palette)
    except Exception as err:
        logger.error(f"Uncaught error during job: {err}")
