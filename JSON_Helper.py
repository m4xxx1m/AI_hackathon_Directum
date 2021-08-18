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


class OutputMultiple(JsonObject):
    text = StringField()
    pages = ObjectListField(Output)


def output_to_json(output):
    output_json = pykson.Pykson().to_json(output)
    return json.dumps(json.loads(output_json), indent=4, ensure_ascii=False)


def output_to_file(output_json, path):
    random.seed()
    chars = ['*', '!', '_', '+', '=', '?', ':']
    while os.path.exists(path + '.json'):
        path += chars[random.randint(0, len(chars))]
    f = open(path + '.json', 'w')
    f.write(output_json)


def join_outputs(outputs):
    if len(outputs) == 1:
        return outputs[0]
    output = OutputMultiple(text='', pages=[])
    for out in outputs:
        output.text += out.text + ' '
        output.pages.append(out)
    return output
