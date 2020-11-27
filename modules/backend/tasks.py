from .celery import app
from .create_gif import start_job

import time
import os


@app.task
def create_zoomgif(name: str, power: int, output_maxsize: int = None):
    src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', "incoming", f"{name}.png"))
    out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', "static", "outputgifs", f"{name}.gif"))
    start_job(src_path, out_path, power, output_maxsize)
    print(f"Completed job! Id: {int(time.time() % 1000)} {src_path}")
