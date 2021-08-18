import spacy
import json


def fourth_task(path, input):
    with open(path + ".json", "r") as read_file:
        recent = json.load(read_file)
    nlp = spacy.load("ru_core_news_sm")
    org = {}
    jstring = {"facts": [org, {}, {}]}
    json.dumps(jstring)
    orgtok, loctok, datetok, montok, pertok = list(), list(), list(), list(), list()
    mounths = ["январ", "феврал", "март", "апрел", "май", "мая", "июн", "июл", "август", "сетябр", "октябр", "ноябр",
               "декаб"]
    years = [str(i) for i in range(1800, 2040)]
    # input = input.replace("\n", " ")
    sentence = input

    doc = nlp(sentence)
    for ent in doc.ents:
        # print(ent.text, ent.start_char, ent.label_)
        if ent.label_ == "ORG":
            orgtok.append([ent.text, ent.start_char])
        if ent.label_ == "PER":
            pertok.append([ent.text, ent.start_char])
        if ent.label_ == "LOC":
            loctok.append([ent.text, ent.start_char])
    orgtext, loctext, datetext, montext, pertext = str(), str(), str(), str(), str()
    for i in range(len(orgtok)):
        orgtext += orgtok[i][0] + " "
    for i in range(len(loctok)):
        loctext += loctok[i][0] + " "
    text = sentence.split(" ")
    for i in range(len(text)):
        if text[i].isdigit() is True and 1800 < int(text[i]) < 2040:
            datetext += text[i] + " "
            datetok.append([text[i], str(sentence.index(text[i]))])
        if text[i].count(".") == 2 or text[i].count(".") == 3:
            res_str = text[i].replace('.', '')
            if res_str.isdigit() is True:
                datetext += text[i] + " "
                datetok.append([text[i], str(sentence.index(text[i]))])
        elif "руб" in text[i] or "₽" in text[i]:
            montext += text[i] + " "
            montok.append([text[i], str(sentence.index(text[i]))])
        else:
            for j in range(len(mounths)):
                if mounths[j] in text[i]:
                    datetext += text[i] + " "
                    datetok.append([text[i], str(sentence.index(text[i]))])
    for i in range(len(pertok)):
        pertext += pertok[i][0] + " "
    org = {"text": orgtext,
           "tag": 'ORGANIZATION',
           "tokens": []}
    loc = {"text": loctext,
           "tag": 'LOCATION',
           "tokens": []}
    date = {"text": datetext,
            "tag": 'DATE',
            "tokens": []}
    money = {"text": montext,
             "tag": 'MONEY',
             "tokens": []}
    person = {"text": pertext,
              "tag": 'PERSON',
              "tokens": []}
    for i in range(len(orgtok)):
        token = {"text": orgtok[i][0],
                 "offset": orgtok[i][1]}
        org["tokens"].append(token)
    for i in range(len(loctok)):
        # print('asddc')
        token = {"text": loctok[i][0],
                 "offset": loctok[i][1]}
        loc["tokens"].append(token)
    for i in range(len(montok)):
        token = {"text": montok[i][0],
                 "offset": montok[i][1]}
        money["tokens"].append(token)
    for i in range(len(datetok)):
        token = {"text": datetok[i][0],
                 "offset": datetok[i][1]}
        date["tokens"].append(token)
    for i in range(len(pertok)):
        token = {"text": pertok[i][0],
                 "offset": pertok[i][1]}
        person["tokens"].append(token)
    jstring = {"facts": [org, loc, date, money, person]}
    recent.update(jstring)
    with open(path + ".json", "w") as write_file:
        json.dump(recent, write_file, ensure_ascii=False, indent=4)
        write_file.close()
    read_file.close()
