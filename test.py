from os import path, mkdir
print(path.join(path.dirname(__file__) + "/rsimg/" + "test.img"))

base_dir = '/rsimg/'

def check_img_dir():
    if not path.isdir(path.join(path.dirname(__file__) + base_dir)):
        mkdir(path.join(path.dirname(__file__) + base_dir))

check_img_dir()
