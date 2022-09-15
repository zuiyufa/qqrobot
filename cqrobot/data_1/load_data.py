 #coding=utf-8
from importlib.resources import read_binary
import os
import json
def read_file():
	data = []
	for count ,line in enumerate(open("/root/cqrobot/data_1/talk_data/words", 'r', encoding='UTF-8')):
		temp = line.strip().split("|")
		temp = [temp[0],temp[1].split("/")[:-1]]
		data.append(temp)
	return data

# a=read_file()
# print(a)
# # ./data_1/talk_data/words