import requests
import json
import csv
import rfc6266
from os import path
import time
import re

data_file = 'rs_data.dat'
filefile = 0
base_link = 'http://2007.runescape.wikia.com/api/v1/Articles/AsSimpleJson?id='
findstr = 'wikia.nocookie.net'

f = open(data_file, "r")
csv_reader = csv.reader(f, delimiter=',')

def findkeys(node, kv):
    if isinstance(node, list):
        for i in node:
            for x in findkeys(i, kv):
               yield x
    elif isinstance(node, dict):
        if kv in node:
            yield node[kv]
        for j in node.values():
            for x in findkeys(j, kv):
                yield x

img_list = []
found = 0
total = 0

for row in csv_reader:
    page = requests.get(base_link + str(row[0]), timeout=None)
    data = json.loads(page.text)
    total += 1
    try:
        image_url = data['sections'][0]['images'][0]['src']
    except (IndexError, KeyError) as e:
        did_find = str(data).find(findstr)
        if did_find > 0:
             img_list.append(list(findkeys(data, 'src')))
             found += 1
             print(str(found) +"/"+ str(total))
