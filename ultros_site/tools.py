# coding=utf-8

import string
from random import SystemRandom

__author__ = "Gareth Coles"


random = SystemRandom()
allowed = string.ascii_letters + string.digits + string.punctuation


def make_token():
    return "".join(random.choice(allowed) for x in range(32))
