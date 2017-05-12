# coding=utf-8

__author__ = "Gareth Coles"

from celery import Celery

app = Celery(
    "ultros_site",
    broker="amqp://",
    backend="rpc://",
    include=[
        "ultros_site.tasks.email"
    ]
)

if __name__ == "__main__":
    app.start()
