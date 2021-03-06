import json
import os
import hashlib
import random
import string
from time import time

# path to chain dir
chain_dir = os.curdir + '/chain/'
files = os.listdir(chain_dir)
files = sorted(int(i) for i in files)

def get_hash(file_name):          # hash def \__0__/
	file = open(chain_dir + file_name, 'rb').read()# указываем имя файла, который мы открываем для чтения с указанием папки
	return hashlib.sha256(file).hexdigest()

def check_integrity():
    for file in files[1:]:
        h = json.load(open(chain_dir + str(file)))['hash']
        actual_hash = get_hash(str(file - 1))

        prev_block = str(file -1)

        if h == actual_hash:
            res = 'kk'
        else:
            res = 'corrupted'
        print('block {} is {}'.format(prev_block, res))

def create_account(wallet):
	userid = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(16))
	user = {'index': int(str(files[-1] + 1)),
			'timestamp': time(),
			'userid': userid,
			'wallet': wallet
	}
	with open(chain_dir + str(files[-1] + 1), 'w') as file:
		json.dump(user, file, indent=4, ensure_ascii=False)


def write_block(sender, amount, message, recipient, prev_hash=''):
	prev_file = files[-1]  # последний блок, который находится в папке chain
	file_name = str(prev_file + 1)  # называем след.файл символьным значением
	prev_hash = get_hash(str(prev_file))  # олучаем хэш предыдущего файла

	for file in files[1:]:
		u = json.load(open(chain_dir + str(file)))['userid']
		if u == sender:
			sw = json.load(open(chain_dir + str(file)))['wallet']
			sender_wallet = sw - amount

	for file in files[1:]:
		u = json.load(open(chain_dir + str(file)))['userid']
		if u == recipient:
			rw = json.load(open(chain_dir + str(file)))['wallet']
			recipient_wallet = rw + amount

	block = {'index': int(str(files[-1] + 1)),
			'timestamp': time() ,
			 'sender' : sender,
			 'amount' : amount,
			 'message' : message,
			 'recipient' : recipient,
			 'sender_wallet': sender_wallet,
			 'recipient_wallet': recipient_wallet,
			 'hash': prev_hash}

	with open(chain_dir + file_name, 'w') as file:
		json.dump(block, file, indent=4, ensure_ascii=False)

def main():

	#write_block(input(), int(input()), input(), input())
	# check_integrity()
	create_account(int(input()))


if __name__ == '__main__':
	main()