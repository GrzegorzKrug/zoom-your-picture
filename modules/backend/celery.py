from celery import Celery
from .logger_shared import logger

import time
import os

user = os.getenv('USER', 'admin')
password = os.getenv('PASSWORD', 'mypass')
host = os.getenv('HOSTNAME', 'localhost')
port = os.getenv('PORT', '5672')

broker_url = f'amqp://{user}:{password}@{host}:{port}'

app = Celery("backend",
             broker=broker_url,
             namespace="zoomgif", include=["backend.tasks"])
app.conf.timezone = 'UTC'


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10 * 60, remove_old_pics.s(), name='clear pictures every 10 min')

    # # Executes every Monday morning at 7:30 a.m.
    # sender.add_periodic_task(
    #     crontab(hour=7, minute=30, day_of_week=1),
    #     test.s('Happy Mondays!'),
    # )


@app.task
def remove_old_pics(maxAge=60 * 60):
    work_dirs = [
            os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'incoming')),
            os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static', 'outputpics'))
    ]
    count_files = 0

    for wk in work_dirs:
        for fl in os.listdir(wk):
            file_path = os.path.join(wk, fl)

            creationtime = os.path.getmtime(file_path)
            age = round(time.time()) - round(creationtime)
            if age > maxAge:
                print(f"Removing file: {file_path}")
                try:
                    os.remove(file_path)
                    count_files += 1
                except Exception:
                    logger.error(f"Error when removing file: {file_path}")
    if count_files > 0:
        logger.info(f"Removed {count_files} files")


if __name__ == "__main__":
    app.start()
