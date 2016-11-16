import requests
import json
import csv
import rfc6266
from os import path, mkdir
import queue
from threading import Thread

data_file = 'rs_data.dat'
base_link = 'http://2007.runescape.wikia.com/api/v1/Articles/AsSimpleJson?id='
dirname = 'rsimg'
base_dir = '/'+ dirname +'/'
que = queue.LifoQueue()

def check_img_dir():
    if not path.isdir(path.join(path.dirname(__file__) + base_dir)):
        mkdir(path.join(path.dirname(__file__) + base_dir))

def queue_factory(data_file):
    f = open(data_file, "r")
    csv_reader = csv.reader(f, delimiter=',')
    for row in csv_reader:
        que.put(base_link + row[0])

def check_file_exists(filename):
    if path.isfile(filename):
        print("FILE EXISTS")
        return True
    else:
        return False

def do_task():
    while not que.empty():
        url = que.get()
        page = requests.get(url, timeout=None)
        data = json.loads(page.text)
        title = data['sections'][0]['title'][0]
        try:
            image_url = data['sections'][0]['images'][0]['src']
            image_data = requests.get(image_url)
            img_filename = rfc6266.parse_requests_response(image_data).filename_unsafe
            if check_file_exists(img_filename):
                que.task_done()
            if not check_file_exists(img_filename):
                write_path = path.join(path.dirname(__file__) + base_dir + img_filename)
                print(write_path)
                with open(write_path, 'wb') as img_file:
                    img_file.write(image_data.content)
                    img_file.close()
                print("WROTE: " + title)
            else:
                print("LARGE ERROR")
        except (IndexError, KeyError) as e:
            print("ERROR: " + title.rjust(20))
    que.task_done()

def main():
    check_img_dir() # this is to make sure the dir exists
    try:
        queue_factory(data_file)
        for i in range(25): # aka number of threadtex
            t1 = Thread(target = do_task) # target is the above function
            t1.start() # start the thread
        que.join()
    except KeyboardInterrupt:
        raise

if __name__ == "__main__": main()
