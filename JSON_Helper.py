import json
import random

import pykson
from pykson import JsonObject, IntegerField, StringField, ObjectListField, ObjectField
import os


class Source(JsonObject):
    width = IntegerField()
    height = IntegerField()
    type = StringField()


class Output(JsonObject):
    text = StringField()
    source = ObjectField(Source)


def output_to_json(output):
    output_json = pykson.Pykson().to_json(output)
    print(output.text)
    return json.dumps(json.loads(output_json), indent=4, ensure_ascii=False)


def output_to_file(output_json, path):
    random.seed()
    chars = ['*', '!', '_', '+', '=', '?', ':', '%']
    while os.path.exists(path + '.json'):
        path += chars[random.randint(0, len(chars))]
    f = open(path + '.json', 'w')
    f.write(output_json)
