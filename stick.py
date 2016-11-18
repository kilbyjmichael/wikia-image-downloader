from pytg import Telegram
from os import listdir
from os.path import isfile, join
from itertools import zip_longest, chain
import time
import shutil

tg = Telegram(
telegram="/home/kilby2/tg/bin/telegram-cli",
pubkey_file="/home/kilby2/tg/tg-server.pub")
receiver = tg.receiver
sender = tg.sender
stickers = "Stickers"
MAX_PACK_SIZE = 100
smile = u'\U0001F3C1'
base_dir = '/home/kilby2/ch/'

pack_name = 'test'

def send_sticker_pack(zipped_list):
	counter = 1
	for png in zipped_list:
		print(base_dir)
		sender.send_document(stickers, base_dir + png)
		time.sleep(1)
		sender.send_msg(stickers, smile)
		time.sleep(1)
		print(str(counter) + "\t" + png)
		shutil.move(base_dir + png, '/home/kilby2/fin/' + png)
		counter += 1

def new_pack(pack_name):
	sender.send_msg(stickers, '/newpack')
	sender.send_msg(stickers, pack_name)
'''
def split_list(img_list):
	list_total_length = len(img_list)
	return zip_longest(*[iter(img_list)]*MAX_PACK_SIZE)
'''
def main():
	pack_link = ''.join(pack_name.split())
	
	doc_list = [f for f in listdir(base_dir) if isfile(join(base_dir, f))]
	#zipper = split_list(doc_list)	
	#new_zipper = []
	#for ele in zipper:
	#	new_zipper.append(ele)
	
	new_zipper = doc_list
	num_packs = len(new_zipper)
	
	linklistadder = []
	
	new_pack(pack_name)
	send_sticker_pack(new_zipper)
	time.sleep(1)
	sender.send_msg(stickers, '/publish')
	time.sleep(1)
	sender.send_msg(stickers, pack_link) #link
	linklistadder.append("https://telegram.me/addstickers/" + pack_link)
	print("https://telegram.me/addstickers/" + pack_link)
	time.sleep(3)
		
	for link in linklistadder:
		print(link)
			
if __name__ == "__main__": main()
