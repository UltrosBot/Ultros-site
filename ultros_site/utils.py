# coding=utf-8
import datetime
import inflect

inflect_engine = inflect.engine()

__author__ = "Gareth Coles"


def format_date_frontend(dt=None):
    if not dt:
        dt = datetime.datetime.now()

    day = inflect_engine.ordinal(dt.day)

    return dt.strftime(
        "{} %B %Y".format(day)
    )
