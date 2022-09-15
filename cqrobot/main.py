 #coding=utf-8
print("0")
from receive import rev_msg
print("1")
from massage_flide import msg_talker
print("2")
talker = msg_talker()
print("3")
print("start")
while True:
    try:
        rev = rev_msg()
        if rev == None:
            continue
    except:
        continue
    if rev["post_type"] == "message":
        #print(rev) #需要功能自己DIY
        if rev["message_type"] == "private": #私聊
            talker.private_msg(rev)
        elif rev["message_type"] == "group": #群聊
            talker.group_msg(rev)
        else:
            continue
    elif rev["post_type"] == "notice":
        if rev["notice_type"] == "group_upload":  # 有人上传群文件
            continue
        elif rev["notice_type"] == "group_decrease":  # 群成员减少
            continue
        elif rev["notice_type"] == "group_increase":  # 群成员增加
            continue
        elif rev["notice_type"] == "notify":
            if rev["sub_type"] == "poke":
                print("确定为戳一戳事件")
                talker.recognize_msg(rev)
        else:
            continue
    elif rev["post_type"] == "request":
        if rev["request_type"] == "friend":  # 添加好友请求
            talker.addFriends(rev)
        if rev["request_type"] == "group":  # 加群请求
            pass
    else:  # rev["post_type"]=="meta_event":
        continue
