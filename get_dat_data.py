import requests
import json
import csv

api_list = 'http://2007.runescape.wikia.com/api/v1/Articles/List?limit=20828'

api_page = requests.get(api_list)
json_list = json.loads(api_page.text)

id_list = []

for element in json_list['items']:
    id_list.append(element['id'])

with open('rs_data.dat', 'w') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL, lineterminator='\n')
    for ele in id_list:
        writer.writerow([ele])
