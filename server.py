import socket
import tkinter as tk
from socket import *
import threading
import queue
import json  # json.dumps(some)打包  json.loads(some)解包
import os
import os.path
import sys
IP = '127.0.0.1'
PORT = 8000  # 端口
messages = queue.Queue()    #存放总体数据
users = []
lock = threading.Lock()             #线程锁
BUFLEN=512

def Current_users():  # 统计当前在线人员
    current_suers = []
    for i in range(len(users)):
        current_suers.append(users[i][0])      #存放用户相关名字
    return  current_suers

class ChatServer(threading.Thread):
    global users, que, lock

    def __init__(self):  # 构造函数
        threading.Thread.__init__(self)
        self.s = socket(AF_INET, SOCK_DGRAM)      #用UDP连接

    def receive(self):  # 接收消息
        while True:
            Info, addr = self.s.recvfrom(1024)  # 收到的信息
            Info_str = str(Info, 'utf-8')
            userIP = addr[0]
            userPort = addr[1]
            print('Info_str:{Info_str},addr:{addr}')
            #接收到“你好~用户b~0”，分割成
            #“你好”，“用户b”，“0”三个信息
            #第一个字符串是用户发送的聊天内容
            #第二个字符串是发送该聊天内容的用户名
            #第三个字符串的0代表是群发
            if '~0' in Info_str:
                data = Info_str.split('~')
                print("data_after_slpit:", data)  # data_after_slpit: ['cccc', 'a', '0']
                message = data[0]   # data
                userName = data[1]  # name
                chatwith = data[2]  # 0
                message = userName + '~' + message + '~' + chatwith
                self.Load(message, addr)
            elif '~' in Info_str and '0' not in Info_str:# 私聊
                data = Info_str.split('~')
                print("data_after_slpit:", data)  # data_after_slpit: ['cccc', 'a', 'destination_name']
                message = data[0]  # data
                userName = data[1]  # name
                chatwith = data[2]  # destination_name
                message = userName + '~' + message + '~' + chatwith
                self.Load(message, addr)
            else:# 新用户
                tag = 1
                temp = Info_str
                for i in range(len(users)):  # 检验重名，则在重名用户后加数字
                    if users[i][0] == Info_str:
                        tag = tag + 1
                        Info_str = temp + str(tag)
                users.append((Info_str, userIP, userPort))
                Info_str = Current_users()  # 当前用户列表
                self.Load(Info_str, addr)
    # 在获取用户名后便会不断地接受用户端发来的消息，结束后关闭连接。
    # 将地址与数据（需发送给客户端）存入messages队列。
    def Load(self, data, addr):
        lock.acquire()
        try:
            messages.put((addr, data))
        finally:
            lock.release()

    # 服务端在接受到数据后，会对其进行一些处理然后发送给客户端
    def sendData(self):  # 发送数据
        while True:
            if not messages.empty():                        #如果信息不为空
                message = messages.get()
                if isinstance(message[1], str):             #判断类型是否为字符串
                    for i in range(len(users)):
                        data = ' ' + message[1]
                        self.s.sendto(data.encode(),(users[i][1],users[i][2])) #聊天内容发送过去
                if isinstance(message[1], list):
                    print("message[1]",message[1])      #message[1]为用户名 message[0]为地址元组
                    data = json.dumps(message[1])
                    for i in range(len(users)):
                        try:
                            self.s.sendto(data.encode(), (users[i][1], users[i][2]))
                        except:
                            pass
    def run(self):
        self.s.bind((IP, PORT))         #绑定端口
        q = threading.Thread(target=self.sendData)  #开启发送数据线程
        q.start()
        t = threading.Thread(target=self.receive)  # 开启接收信息进程
        t.start()

#入口
if __name__ == '__main__':
    cserver = ChatServer()
cserver.start()

