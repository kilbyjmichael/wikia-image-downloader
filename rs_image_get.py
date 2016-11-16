import requests
import json
import csv
import rfc6266
from os import path
import time

data_file = 'rs_data.dat'

base_link = 'http://2007.runescape.wikia.com/api/v1/Articles/AsSimpleJson?id='

f = open(data_file, "r")
csv_reader = csv.reader(f, delimiter=',')

def check_file_exists(filename):
    if path.isfile(filename):
        print("FILE EXISTS")
        time.sleep(1)
        return True
    else:
        return False

for row in csv_reader:
    page = requests.get(base_link + str(row[0]), timeout=None)
    data = json.loads(page.text)
    try:
        image_url = data['sections'][0]['images'][0]['src']
        image_file = requests.get(image_url)
        imgfname = rfc6266.parse_requests_response(image_file).filename_unsafe
        #print(check_file_exists(imgfname))
        with open(imgfname, 'wb') as img_file:
            img_file.write(image_file.content)
            img_file.close()
            #print(str(check_file_exists(imgfname)) + '\n')

    except (IndexError, KeyError) as e:
        pass
