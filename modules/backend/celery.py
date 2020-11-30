from celery import Celery

import os

user = os.getenv('USER', 'admin')
password = os.getenv('PASSWORD', 'mypass')
host = os.getenv('HOSTNAME', 'localhost')
port = os.getenv('PORT', '5672')

broker_url = f'amqp://{user}:{password}@{host}:{port}'

app = Celery("backend",
             broker=broker_url,
             namespace="zoomgif", include=["backend.tasks"])
app.conf.update(result_expires=1 * 3600)

if __name__ == "__main__":
    app.start()
