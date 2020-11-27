from .celery import app


@app.task
def start_gifzoom(name: str, power: int, output_maxsize: int):
    print("started job!")

