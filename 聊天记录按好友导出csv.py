import pandas as pd
import numpy as np
import csv
from pathlib import Path
import time, datetime
import json
import xmltodict

addr = r'C:\Users\Gavin\Desktop\20210805微信聊天记录导出备份'

# 读取聊天记录
message = pd.read_csv(addr + '\message.csv', encoding='ANSI', low_memory=False)
message = message[['talker', 'isSend', 'createTime', 'content', 'type', 'imgPath']].sort_values(by='createTime', ascending=True)  # ascending=True
# print(message)
message = message.values.tolist()

# 读取联系人信息
friend = pd.read_csv(addr + '\\rcontect.csv', encoding='ANSI')
friend = friend[['username', 'conRemark', 'nickname', 'quanPin', 'type']].values.tolist()

# 建立联系人索引
contect = {}
for row in friend:
    _row = row
    try:
        if (np.isnan(row[1])):
            _row[1] = ''
    except:
        pass
    try:
        if (np.isnan(row[2])):
            _row[2] = ''
    except:
        pass
    contect[row[0]] = _row
# print(contect)

chat = {}
# 建立聊天记录索引
# ['talker', 'conRemark' or 'nickname', 'isSend', 'createTimeStamp', 'createTime' , 'content', 'isReply', 'citeTalker', 'cite', 'type', 'imgPath']
for row in message:
    _row = row
    # 添加备注或昵称
    try:
        _row.insert(1, contect[row[0]][1] if contect[row[0]][1]!='' else contect[row[0]][2])
    except:
        _row.insert(1, np.nan)

    # 时间戳还原
    timeArray = time.localtime(int(int(row[3])/1000))
    Time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    _row.insert(4, Time)

    # 解析引用的情况
    try:
        if np.isnan(row[5]):
            _row.insert(6, 0)
            _row.insert(7, '')
            _row.insert(8, '')
        else:
            _row.insert(6, 0)
            _row.insert(7, '')
            _row.insert(8, '')
    except:
        if len(str(row[5])) > 500:
            content = row[5]
            try:
                content = json.loads(json.dumps(xmltodict.parse(content)))
                refer = content['msg']['appmsg']['refermsg']['content']
                reply = [content['msg']['appmsg']['title'], content['msg']['appmsg']['refermsg']['displayname'], refer]
                if len(str(refer)) > 500:
                    try:
                        content = json.loads(json.dumps(xmltodict.parse(refer)))
                        refer = content['msg']['appmsg']['title']
                        reply[2] = refer
                    except:
                        pass
                _row[5] = reply[0]
                _row.insert(6, 1)
                _row.insert(7, reply[1])
                _row.insert(8, reply[2])
            except:
                _row.insert(6, 0)
                _row.insert(7, '')
                _row.insert(8, '')
        else:
            _row.insert(6, 0)
            _row.insert(7, '')
            _row.insert(8, '')


    if row[0] in chat.keys():
        chat[row[0]].append(_row)
    else:
        chat[row[0]] = [_row]
# print(chat)

# 保存文件
header = ['talker', 'conRemark' or 'nickname', 'isSend', 'createTimeStamp', 'createTime' , 'content', 'isReply', 'citeTalker', 'cite', 'type', 'imgPath']
for k in chat.keys():
    print(k)
    if contect[k][1] == '' and contect[k][2] == '':
        filename = k
    else:
        filename = contect[k][1] if contect[k][1] != '' else contect[k][2]

    filename = filename.replace('?', '(emoji)')
    filename = filename.replace(':', '：')
    filename = filename.replace('/', '(sign)')
    filename = filename.replace('\\', '(sign)')
    filename = filename.replace('|', '(sign)')
    filename = filename.replace('<', '(sign)')
    filename = filename.replace('>', '(sign)')
    filename = filename.replace('[', '(sign)')
    filename = filename.replace(']', '(sign)')

    if k[-9:-1] == '@chatroo':
        filename = '0_chatroom-' + filename

    if k[0:3] == 'gh_':
        filename = '0_gzh-' + filename

    file = Path('save\\' + filename + '.csv')
    while file.is_file():
        filename = filename + '-a'
        file = Path('save\\' + filename + '.csv')

    with open('save\\'+ filename +'.csv', 'w', encoding='ANSI', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(header)
        f_csv.writerows(chat[k])
