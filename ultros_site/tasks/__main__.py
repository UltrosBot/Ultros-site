# coding=utf-8
from celery import Celery

__author__ = "Gareth Coles"


app = Celery(
    "ultros_site",
    broker="amqp://",
    backend="redis://localhost:6379/0",
    include=[
        "ultros_site.tasks.email"
    ]
)

if __name__ == "__main__":
    app.start()
