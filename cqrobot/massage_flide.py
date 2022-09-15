 #coding=utf-8
print('step0')
import json
print("0")
from data_1.load_data import read_file
print("1")
from data_1.load_reply import read_reply
print("2")
from send_message.send_message import send_message
print("3")
from send_message.talk_to_user import *
print("4")
from random import randint
print("step1")
self_qq = json.load(open("/root/cqrobot/config.json", encoding='utf-8'))["self_qq"]
print("step2")
ban_words = json.load(open("/root/cqrobot/config.json", encoding='utf-8'))["ban_words"]
print("step3")
class msg_talker():
	def __init__(self):
		self.talk_data = read_file()
		self.reply_data= read_reply()
		self.States={}

	def private_msg(self,rev):
		if rev["sub_type"] != "friend":
			return send_message('你还不是我的好友呀',rev['user_id'],"private")
		return send_message(talk_to_user(rev, self.talk_data,self.reply_data,self.States), rev["user_id"], "private")

	def group_msg(self,rev):
		if "[CQ:at,qq={}]".format(self_qq) in rev["raw_message"]:
			try:
				rev['raw_message']=rev['raw_message'].split(" ")[1]
			except:
				pass
			return send_message(talk_to_user(rev, self.talk_data,self.reply_data,self.States), rev["group_id"], "group")

		if "[CQ:image" in rev["raw_message"] and rev["user_id"] in self.States and self.States[rev["user_id"]]=="WFPS":
			print("识别到识图用户发的图了")
			return send_message(talk_to_user(rev, self.talk_data,self.reply_data,self.States), rev["group_id"], "group")

		for words in ban_words:
			if words in rev['raw_message']:	
				return send_message(talk_to_gourp(rev, self.talk_data), rev["group_id"], "group")
		
		if "raw_message" in rev:			
			try:
				rev['raw_message']=rev['raw_message'].split(" ")[1]
			except:
				pass
			return send_message(talk_to_qunyou(rev,self.reply_data,self.talk_data,self.States), rev["group_id"], "group")
		return True
		
	def addFriends(self,rev):
		return send_message(add_friends(rev), rev["user_id"], "friends")

	def recognize_msg(self,rev):
		print(rev["target_id"])
		if rev["target_id"]==int(self_qq):
			if "group_id" in rev:
				return send_message(talk_to_user(rev,self.talk_data,self.reply_data,self.States),rev["group_id"],"group")
			elif "group_id" not in rev:
				return send_message(talk_to_user(rev,self.talk_data,self.reply_data,self.States),rev["user_id"],"private")

		