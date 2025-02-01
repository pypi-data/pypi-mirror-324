#!/usr/bin/env python
# coding: utf-8

import datetime
import json
import random
import time
from typing import Tuple
import re

from . import constants
from .constants import CustomJSONEncoder, Message


def parse_broker_url(broker_url) -> Tuple[str, int]:
    strs = broker_url.split(":")
    if len(strs) > 1:
        host = strs[0]
        port = int(strs[1])
    else:
        host = broker_url
        port = 1883

    return host, port


def get_message_id():
    return "%0.f-%d" % (time.time() * 100000, random.randint(0, 9))


def parse_topic(topic):
    return topic.split("/")


def json_dumps(data):
    return json.dumps(data, ensure_ascii=False)


def json_loads(data):
    return json.loads(data)


def json_encode(data, cls=CustomJSONEncoder):
    return json.dumps(data, cls=cls, ensure_ascii=False)


def message_hook(d):
    return Message(**d)


def json_decode(data, object_hook=message_hook):
    return json.loads(data, object_hook=object_hook)


def new_message(**kwargs) -> Message:
    return Message(get_message_id(), **kwargs)


def format_mac(mac, sep=':'):
    mac = re.sub("[^0-9A-Fa-f]", "", mac)
    return (
        sep.join([mac[i : i + 2] for i in range(0, 12, 2)]) if len(mac) == 12 else mac
    ).upper()


def clear_colon(input_string):
    return input_string.replace(":", "")


def response(id="", cmd="", *, code=0, data={}, msg={}):
    _data = {"code": code}
    if data:
        _data["data"] = data

    if msg:
        _data["msg"] = msg

    return {"id": id, "cmd": cmd, "data": _data}


def date_hour():
    now = datetime.datetime.now()

    return now.strftime("%Y-%m-%d"), now.strftime("%H")


def now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def after(**kwargs):
    return (datetime.datetime.now() + datetime.timedelta(**kwargs)).strftime(
        "%Y-%m-%d %H:%M:%S"
    )


def timestamp():
    return int(time.time())
