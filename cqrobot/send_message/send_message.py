 #coding=utf-8
import requests
import json

def send_message(msg,qq_id,qq_type):
	if msg=="" or msg==None:
		pass
	
	elif qq_type == "private":
		data = {
			'user_id':qq_id,
			'message':msg,
			'auto_escape':False
		}
		cq_url = "http://127.0.0.1:5700/send_private_msg"
		rev = requests.post(cq_url,data=data)
	elif qq_type == "group":
		data = {
			'group_id':qq_id,
			'message':msg,
			'auto_escape':False
		}
		cq_url = "http://127.0.0.1:5700/send_group_msg"
		rev = requests.post(cq_url,data=data)
	elif qq_type == "friends":
		data = {
			'approve':msg['isOK'],
			'flag':msg['flag'],
			'remark':msg['friendsName']
		}
		cq_url = "http://127.0.0.1:5700/set_friend_add_request"
		rev = requests.post(cq_url, data=data)
	else:
		return False
	# print(rev.json())
	# if rev.json()['status'] == 'ok':
	# 	return True
	return True