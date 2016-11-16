import requests
import json
import csv
import rfc6266

data_file = 'rs_data.test'

base_link = 'http://2007.runescape.wikia.com/api/v1/Articles/AsSimpleJson?id='

f = open(data_file, "r")
csv_reader = csv.reader(f, delimiter=',')

for row in csv_reader:
    page = requests.get(base_link + str(row[0]), timeout=None)
    data = json.loads(page.text)
    try:
        image_url = data['sections'][0]['images'][0]['src']
        image_file = requests.get(image_url)        
        with open(rfc6266.parse_requests_response(image_file).filename_unsafe, 'wb') as img_file:
            img_file.write(image_file.content)
    except (IndexError, KeyError) as e:
        pass
