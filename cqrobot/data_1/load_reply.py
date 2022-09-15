 #coding=utf-8
import os
import json
def read_reply():
    val=[]
    for row ,line in enumerate(open("/root/cqrobot/data_1/talk_data/reply", 'r')):
        temp = line.strip().split("\n")
        # print(temp)
        for i in temp:
            if i!='':
                val.append(i)
    dic1={}
    n=len(val)
    for i in range(0,n,2):
        key=val[i]
        value=val[i+1]
        if not key in dic1:
            dic1[key]=[]
        dic1[key].append(value)
    return dic1






