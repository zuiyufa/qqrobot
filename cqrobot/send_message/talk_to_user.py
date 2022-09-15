 #coding=utf-8

from logging import StringTemplateStyle
from sre_parse import State
import sys
from os import path
d = path.dirname(__file__) # 获取当前路径
sys.path.append(d) # 如果要导入到包在上一级
print("0")
from random import randint
print("0")
from random import choice
print("1")
from base_talk import others_answer
print("2")
from word_detect import *
print("3")
from send_message.send_message import send_message
print("4")
from SauceNAO import *
print("5")
import time
print("1")

def match(msg,talk_data):
    for row in talk_data:
        if row[0] in msg:
            n=len(row[1])-1
            if n==0:
                return [True,row[1][0]]
            else:
                num=randint(0,n)
                return [True,row[1][num]]
    return [False,choice(others_answer["no_answer"])]

def match1(msg,reply_data):
    if msg in reply_data:
        n=len(reply_data[msg])-1
        if n==0:
            return[True,reply_data[msg][0]]
        else:
            index=randint(0,n)
            return[True,reply_data[msg][index]]
    return[False,""]







def talk_to_user(rev,talk_data,reply_data,States):#这里可以DIY对私聊和群聊中@yes酱的操作
    #--------------------------------------------------------------------------------------
    if_pre = prepa(rev,States)
    if if_pre[0] == True:
        return if_pre[1]
    #---------------------------------------------------------------------------------------
    if_con = consult(rev,States)
    if if_con[0] == True:
        return if_con[1]
    #-----------------------------------------------------------------------------------------
    if "raw_message" in rev:
        msg=rev["raw_message"]
        #--------------------------------------------------------------------------------------帮助页面
        if_help = help_menu(msg)
        if if_help[0] == True:
            return if_help[1]
        #--------------------------------------------------------------------------------------删除数据
        if_del = del_data(msg,talk_data)
        if if_del[0] == True:
            return if_del[1]
        #--------------------------------------------------------------------------------------添加数据
        if_add = add_data(msg,talk_data)
        if if_add[0] == True:
            return if_add[1]
        #--------------------------------------------------------------------------------------发送涩图
        if_setu = ghs_pic(msg)
        if if_setu[0] == True:
            return if_setu[1]
        #--------------------------------------------------------------------------------------发送R18
        if_setu = hs_pic(msg)
        if if_setu[0] == True:
            return if_setu[1]
        #--------------------------------------------------------------------------------------发送猫猫图
        if_setu = mao_pic(msg)
        if if_setu[0] == True:
            return if_setu[1]
        #------------------------------
        if_setu = gdhs_pic(msg)
        if if_setu[0] == True:
            return if_setu[1]
        #------------------------------
        if_setu = gjsshs_pic(msg)
        if if_setu[0] == True:
            print("发送完成")
            return if_setu[1]
        #------------------------------
        if_setu = chaijun_pic(msg)
        if if_setu[0] == True:
            return if_setu[1]
        #--------------------------------
        if_setu = garden_pic(msg)
        if if_setu[0] == True:
            return if_setu[1]
        #---------------------------------
        if_setu = maomaochong_pic(msg)
        if if_setu[0] == True:
            return if_setu[1]
        #------------------------------------------------------------
        if_lvcha = lvcha(msg)
        if if_lvcha[0] == True:
            return if_lvcha[1]

    return match(msg,talk_data)[1]

def talk_to_gourp(rev,talk_data):#这里可以DIY对群聊的操作
    msg=rev["raw_message"]
    user_id=rev["user_id"]
    group_id=rev["group_id"]
    #--------------------------------------------------------------------------------------检测关键字禁言
    if_ban = detect_ban(msg,user_id,group_id)
    if if_ban[0] == True:
        return if_ban[1]
    if match(msg,talk_data)[0]==True:
        return match(msg,talk_data)[1]
    return ""

def talk_to_qunyou(rev,reply_data,talk_data,States):
    # print("进talk to qunyou")
    msg=rev["raw_message"]
    result=consult(rev,States)
    if result[0]==True:
        print(result)
        return result[1]
    if match(msg,talk_data)[0]==True:
        return match(msg,talk_data)[1]
    if_lvcha = lvcha(msg)
    if if_lvcha[0] == True:
        return if_lvcha[1]
    
    return match1(msg,reply_data)[1]

def prepa(rev,States):
    if "sender_id" in rev:
        sender_id=rev["sender_id"]
        if sender_id not in States:
            print("用户id加入States字典")
            States[sender_id]="Normal"
        if rev["notice_type"] == "notify":
            print("将用户状态转换为等待识图")
            States[sender_id]="WFPS"
            return [True,"发送一张图片开始识图"]
    return [False]
    
def consult(rev,States):
    msg= rev["raw_message"]
    # print("进来了")
    if rev["user_id"] in States:
        sender_id=rev["user_id"]
        if States[sender_id]=="WFPS":
            print("识别到准备识图的用户")
            if "[CQ:image" in msg:
                print('识别到图片')
                States[sender_id]="Normal"
                result=SauceNao(msg)
                if result[0]==True:
                    return [True,result[1]]
                elif result[0]==False:
                    return [True,result[1]]
            else:
                print('取消搜图')
                States[sender_id]="Normal"
                return [True,"取消搜图"]
    return [False]

def add_friends(rev):#这里可以DIY对添加好友的操作
    print(rev)
    sender = rev['user_id']
    msg = rev['comment']
    if_add = add_friend(sender,msg)
    obj = {
        'isOK': if_add[0],
        'flag': rev['flag'],
        'friendsName': if_add[1]
    }
    return obj

