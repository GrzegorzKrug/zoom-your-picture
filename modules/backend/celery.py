from celery import Celery

import os

user = os.getenv('LOGIN', 'admin')
password = os.getenv('PASSWORD', 'mypass')
hostname = os.getenv('HOSTNAME', 'localhost')
port = os.getenv('PORT', '5673')

broker_url = f'amqp://{user}:{password}@{hostname}:{port}'

app = Celery("backend", namespace="zoomgif", include=["backend.tasks"])
app.conf.update(result_expires=3*3600)

if __name__ == "__main__":
    app.start()

