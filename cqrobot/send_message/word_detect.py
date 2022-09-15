 #coding=utf-8
from operator import contains
import requests
import json
import os
import re
from random import choice

from send_message.send_message import send_message
group = json.load(open("/root/cqrobot/config.json", encoding='utf-8'))["group"]
apikey= json.load(open("/root/cqrobot/config.json", encoding='utf-8'))["apikey"]
ban_words = json.load(open("/root/cqrobot/config.json", encoding='utf-8'))["ban_words"]
path = json.load(open("/root/cqrobot/config.json", encoding='utf-8'))["path"]
chaijunpath = json.load(open("/root/cqrobot/config.json", encoding='utf-8'))["chaijunpath"]
gardenpath = json.load(open("/root/cqrobot/config.json", encoding='utf-8'))["gardenpath"]
maomaochongpath = json.load(open("/root/cqrobot/config.json", encoding='utf-8'))["maomaochongpath"]
addfriend_word = json.load(open("/root/cqrobot/config.json", encoding='utf-8'))["addfriend_word"]


help_base = "这里是帮助菜单：\n"
help_base += "1.发送 setu 或者 猫猫图 即可返回一张图\n"
help_base += "2.私聊调教对话 例如aaa+bbb \n"
help_base += "那么发送aaa就会返回bbb啦~\n"
help_base += "可以发送rmaaa+bbb删除对话哦~\n"
help_base += "3.发送setu=标签 就可以搜索了\n"
help_base += "最多三个标签,每个标签中间用-隔开哦\n"
help_base += "4.好友验证信息输入114514即可自动添加\n"
help_base += "5.新增图片识别功能\n"
help_base += "戳一戳我就可以开始识别图片了哦"



def help_menu(msg):
    if msg[:4]!="help":
        return [False]
    if msg == "help":
        return [True,help_base]
    
def add_data(msg,all_data):
    if msg.count("+") != 1:
        return [False]
    if "/" in msg or "|" in msg:
        return [True,"不能含有/或|呀~"]
    if msg.split("+")[1]=="":
        return [False]
    msg = msg.split("+")
    if len(msg[0])< 3:
        return [True,"长度要大于2呀~"]
    for row in all_data:
        if msg[0] == row[0]:
            if msg[1] in row[1]:
                return [True,"这句话我已经会辣，不用再教我啦~"]
            row[1].append(msg[1])
            save_data(all_data)
            return [True,"添加成功！"]
    all_data.append([msg[0], [msg[1]]])
    save_data(all_data)
    return [True,"添加成功！"]

def save_data(all_data):
    f = open("./data_1/talk_data/words","w",encoding='UTF-8')
    for row in all_data:
        temp = row[0]+"|"+"".join([i+"/" for i in row[1]])
        f.writelines(temp+"\n")
    f.close()

def del_data(del_data,all_data):
    if del_data[:2] != "rm":
        return [False]
    msg = del_data[2:].split("+")
    for i in range(len(all_data)):
        if msg[0] == all_data[i][0]:
            if len(all_data[i][1]) == 1:
                all_data.pop(i)
                save_data(all_data)
                return [True,"已经删除啦~"]
            all_data[i][1].remove(msg[1])
            save_data(all_data)
            return [True,"已经删除啦~"]
    return [True,"删除出错啦~"]


def ghs_pic(msg):
    
    if msg in ["setu","色图","来张色图","来点色图","来点涩图","涩图","来张涩图"]:
        try:
            req_url="https://api.lolicon.app/setu/v2"
            params = {"r18":"0"}
            res=requests.get(req_url,params=params)
            # print(res)
            # print(res.text)
            html=res.text
            data=json.loads(html)
            print(data)
            data_list = data['data']

            for item in data_list:
                setu_title = item['title']
                setu_pid = item['pid']
                setu_author =item ['author']
                setu_r18=item ['r18']
                originalurl = item['urls']
                setu_url = originalurl['original']
                # print(setu_title)
                # print(setu_pid)
                # print(setu_author)
            print(setu_url)
            if setu_r18==False:
                #local_img_url = "title:"+setu_title+"[CQ:image,file="+setu_url+"]"+"pid:"+str(setu_pid)+" 画师:"+setu_author
                local_img_url = "[CQ:image,file="+setu_url+"]"
            else:
                local_img_url = setu_url
            return [True, local_img_url]
        except Exception as e:
            print(e)
            return [True, "关键词搜索没有结果"]
    return [False]

def gdhs_pic(msg):

    if msg in ["dasetu","大色图","来张大色图","来点大涩图","大涩图","来张大涩图","来点大色图"] or "大色图" in msg or "大涩图" in msg:
        try:
            req_url="https://api.lolicon.app/setu/v2"
            params = {"r18":"0"}
            res=requests.get(req_url,params=params)
            # print(res)
            # print(res.text)
            html=res.text
            data=json.loads(html)
            print(data)
            data_list = data['data']

            for item in data_list:
                setu_title = item['title']
                setu_pid = item['pid']
                setu_author =item ['author']
                setu_r18=item ['r18']
                originalurl = item['urls']
            setu_url = originalurl['original']
            # print(setu_title)
            # print(setu_pid)
            # print(setu_author)
            print(setu_url)
            if setu_r18==False:
                #local_img_url = "title:"+setu_title+"[CQ:image,file="+setu_url+"]"+"pid:"+str(setu_pid)+" 画师:"+setu_author
                local_img_url = "[CQ:cardimage,file="+setu_url+"]"
            else:
                local_img_url = setu_url
            return [True, local_img_url]
        except Exception as e:
            print(e)
            return [True, "阿这，出了一点问题"]
    return [False]

def gjsshs_pic(msg):
    searchobj = re.split('=',msg)
    print(searchobj)
    searchobj1=searchobj[0]+"="
    if searchobj1 in ["setu=","涩图=","色图="]:
        try:
            req_url="https://api.lolicon.app/setu/v2"
            tags=searchobj[1]
            #print(tags)
            tag=re.split('-',tags)
            #print(tag)
            num=len(tag)
            # print(num)
            if num >= 1:
                tag1 = tag[0]
                #print("tag1="+tag1)
                req_url = "https://api.lolicon.app/setu/v2?tag={}".format(tag1)
                if num >= 2:
                    tag2 = tag[1]
                    #print("tag2="+tag2)
                    req_url = "https://api.lolicon.app/setu/v2?tag={}&tag={}".format(tag1, tag2)
                    if num >= 3:
                        tag3 = tag[2]
                        #print("tag3="+tag3)
                        req_url = "https://api.lolicon.app/setu/v2?tag={}&tag={}&tag={}".format(tag1, tag2, tag3)
            #print(req_url)
            params = {"r18":"0"}
            res=requests.get(req_url,params=params)
            # print(res)
            # print(res.text)
            html=res.text
            data=json.loads(html)
            print(data)
            data_list = data['data']

            for item in data_list:
                setu_title = item['title']
                setu_pid = item['pid']
                setu_author =item ['author']
                setu_r18=item ['r18']
                originalurl = item['urls']
            setu_url = originalurl['original']
            # print(setu_title)
            # print(setu_pid)
            # print(setu_author)
            print(setu_url)
            if setu_r18==False:
                #local_img_url = "title:"+setu_title+"[CQ:image,file="+setu_url+"]"+"pid:"+str(setu_pid)+" 画师:"+setu_author
                local_img_url = "[CQ:image,file="+setu_url+"]"
            else:
                local_img_url = setu_url
            return [True, local_img_url]
        except Exception as e:
            print(e)
            return [True, "大概率是没搜到哦"]
    return [False]

def hs_pic(msg):
    searchobj = re.split('=',msg)
    print(searchobj)
    searchobj1=searchobj[0]+"="
    if searchobj1 in ["setur18=","涩图r18=","色图r18="]:
        try:
            req_url="https://api.lolicon.app/setu/v2"
            tags=searchobj[1]
            #print(tags)
            tag=re.split('-',tags)
            #print(tag)
            num=len(tag)
            # print(num)
            if num >= 1:
                tag1 = tag[0]
                #print("tag1="+tag1)
                req_url = "https://api.lolicon.app/setu/v2?tag={}".format(tag1)
                if num >= 2:
                    tag2 = tag[1]
                    #print("tag2="+tag2)
                    req_url = "https://api.lolicon.app/setu/v2?tag={}&tag={}".format(tag1, tag2)
                    if num >= 3:
                        tag3 = tag[2]
                        #print("tag3="+tag3)
                        req_url = "https://api.lolicon.app/setu/v2?tag={}&tag={}&tag={}".format(tag1, tag2, tag3)			
            params = {"r18":"1"}
            res=requests.get(req_url,params=params)
            #print(res)
            #print(res.text)
            html = res.text
            data = json.loads(html)
            #print(data)
            data_list = data['data']

            for item in data_list:
                setu_title = item['title']
                setu_pid = item['pid']
                setu_author = item['author']
                setu_r18=item ['r18']
                originalurl = item['urls']
            setu_url = originalurl['original']
            #print(setu_title)
            #print(setu_pid)
            #print(setu_author)
            print(setu_url)
            if setu_r18==False:
                #local_img_url = "title:"+setu_title+"[CQ:image,file="+setu_url+"]"+"pid:"+str(setu_pid)+" 画师:"+setu_author
                local_img_url = "[CQ:image,file="+setu_url+"]"
            else:
                local_img_url = setu_url
            return [True, local_img_url]
        except Exception as e:
            print(e)
            return [True, "阿这，出了一点问题"]
    return [False]

def mao_pic(msg):
    if msg in ["来张猫猫图", "来张猫图", "猫图", "喵图", "maomao","猫猫图","猫","猫猫"] or "猫猫" in msg:
        setu_list = os.listdir(path)
        # print(setu_list)
        local_img_url = "[CQ:image,file=file://" + path + choice(setu_list) + "]"
        return [True, local_img_url]
    return [False]

def chaijun_pic(msg):
    if msg in ["来张柴郡", "柴郡", "小柴郡", "大柴郡", "chaijun","来点柴郡"] or "柴郡" in msg :
        setu_list = os.listdir(chaijunpath)
        # print(setu_list)
        local_img_url = "[CQ:image,file=file://" + chaijunpath + choice(setu_list) + "]"
        return [True, local_img_url]
    return [False]

def garden_pic(msg):
    if msg in ["来张花园猫", "花园猫", "小花园", "大花园", "hauyuan","来点花园猫","花园"] or "花园" in msg :
        setu_list = os.listdir(gardenpath)
        # print(setu_list)
        local_img_url = "[CQ:image,file=file://" + gardenpath + choice(setu_list) + "]"
        return [True, local_img_url]
    return [False]

def maomaochong_pic(msg):
    if msg in ["来张猫猫虫", "jiabo", "伽波", "咖波", "来张咖波","来点咖波","来点猫猫虫","猫猫虫"] or "猫猫虫" in msg:
        setu_list = os.listdir(maomaochongpath)
        # print(setu_list)
        local_img_url = "[CQ:image,file=file://" + maomaochongpath + choice(setu_list) + "]"
        return [True, local_img_url]
    return [False]

def lvcha(msg):
    if "绿茶" in msg:
        genderType="F"
        url="https://api.lovelive.tools/api/SweetNothings/1/Serialization/Json?genderType={}"
        r=requests.get((url).format(genderType))
        result=json.loads(r.text)
        answer=result['returnObj'][0]
        return [True,answer]
    return [False]
    

def detect_ban(msg,user_id,group_id):
    if group_id not in group:
        return [False]
    for words in ban_words:
        if words in msg:
            data = {
                'user_id':user_id,
                'group_id':group_id,
                'duration':60
            }
            cq_url = "http://127.0.0.1:5700/set_group_ban"
            requests.post(cq_url,data=data)
            return [True,"不要说不该说的话啦~"]
    return [False]

def add_friend(sender,msg):

    try:
        print('add_friends')
        if msg == addfriend_word:
            return [True, sender]
        else:
            return [False, ""]
    except Exception as e:
        print(e)
    return [False, '']