from socket import *
import time
import tkinter
import tkinter.messagebox
import threading
import json
import tkinter.filedialog
from tkinter.scrolledtext import ScrolledText

IP = '127.0.0.1'
SERVER_PORT =8000
user = ''
listbox1 = ''  # 用于显示在线用户的列表框
show = 1  # 用于判断是开还是关闭列表框
users = []  # 在线用户列表
chat = '0'  # 聊天对象
chat_pri = ''

# 登陆窗口
window1 = tkinter.Tk()
window1.geometry("300x250")
window1.title('login')
ip0 = tkinter.StringVar()
ip0.set('')
port0 = tkinter.StringVar()
port0.set('')
user0 = tkinter.StringVar()
user0.set('')
labelIP = tkinter.Label(window1,text='目的ip地址:',width=40,height=2)
labelIP.pack()
entryIP = tkinter.Entry(window1, textvariable=ip0)
entryIP.pack()
labelPORT = tkinter.Label(window1,text='目的端口号:',width=40,height=2)
labelPORT.pack()
entryPORT = tkinter.Entry(window1, textvariable=port0)
entryPORT.pack()
labelUSER = tkinter.Label(window1,text='用户名:',width=40,height=2)
labelUSER.pack()
entryUSER = tkinter.Entry(window1, textvariable=user0)
entryUSER.pack()

def Login():
    global IP, PORT, user
    IP = entryIP.get()
    PORT = entryPORT.get()
    user = entryUSER.get()
    if not IP:
        tkinter.messagebox.showwarning('warning', message='目的IP地址为空!')  # 目的IP地址为空则提示
    elif not PORT:
        tkinter.messagebox.showwarning('warning', message='目的端口号为空!')  # 目的端口号为空则提示
    elif not user:
        tkinter.messagebox.showwarning('warning', message='用户名为空!')     # 客户端用户名为空则提示
    else:
        window1.destroy()

loginButton = tkinter.Button(window1, text="登录", command=Login,)
loginButton.place(x=135, y=200, width=40, height=25)
window1.bind('<Return>', Login)

window1.mainloop()
# 聊天窗口
window2 = tkinter.Tk()
window2.geometry("500x350")
window2.title('聊天界面')

# 消息界面
listbox = ScrolledText(window2)
listbox.place(x=5, y=0, width=350, height=250)
listbox.insert(tkinter.END, '欢迎用户 '+user+' 加入聊天室!')
listbox.insert(tkinter.END, '\n')
# 在线用户列表
listbox1 = tkinter.Listbox(window2)
listbox1.place(x=350, y=0, width=140, height=250)
#输入框
INPUT = tkinter.StringVar()
INPUT.set('')
entryIuput = tkinter.Entry(window2, width=350, textvariable=INPUT)
entryIuput.place(x=5, y=260, width=485, height=50)



#UDP连接部分
ip_port = (IP, int(PORT))
s = socket(AF_INET, SOCK_DGRAM)
if user:
    s.sendto(user.encode(), ip_port)  # 发送用户名
else:
    s.sendto('用户名不存在', ip_port)
    user = IP + ':' + PORT


def send():
    message = entryIuput.get() + '~' + user + '~' + chat
    s.sendto(message.encode(), ip_port)
    INPUT.set('')
    return 'break'  #按回车后只发送不换行

def Priva_window():
    chat_pri = entryPriva_target.get()
    message = entryPriva_talk.get()
    if not chat_pri:
        tkinter.messagebox.showwarning('warning', message='私聊目标名称为空!')  # 目的IP地址为空则提示
    else:
        window3.destroy()
        message = message + '~' + user + '~' + chat_pri
        s.sendto(message.encode(), ip_port)
        INPUT.set('')

def Priva_Chat():
    global chat_pri,window3,Priva_target,labelPriva_target,entryPriva_target,Priva_talk,labelPriva_talk,entryPriva_talk
    window3 = tkinter.Toplevel(window2)
    window3.geometry("300x150")
    window3.title('私聊窗口')
    window = tkinter.Label(window3, width=300, height=150)
    window.pack()
    Priva_target = tkinter.StringVar()
    Priva_target.set('')
    labelPriva_target = tkinter.Label(window3, text='用户名称')
    labelPriva_target.place(x=20, y=5, width=100, height=40)
    entryPriva_target = tkinter.Entry(window3, width=60, textvariable=Priva_target)
    entryPriva_target.place(x=120, y=10, width=100, height=30)

    Priva_talk = tkinter.StringVar()
    Priva_talk.set('')
    labelPriva_talk = tkinter.Label(window3, text='消息内容')
    labelPriva_talk.place(x=20, y=40, width=100, height=40)
    entryPriva_talk = tkinter.Entry(window3, width=60, textvariable=Priva_talk)
    entryPriva_talk.place(x=120, y=45, width=100, height=30)

    Priva_targetButton = tkinter.Button(window3, text="确定", command=Priva_window)
    Priva_targetButton.place(x=135, y=90, width=40, height=25)


sendButton = tkinter.Button(window2, text="发送", anchor='n', command=send)
sendButton.place(x=100, y=320, width=50, height=28)

PrivaButton = tkinter.Button(window2, text="私聊", anchor='n', command=Priva_Chat)
PrivaButton.place(x=300, y=320, width=50, height=28)
window2.bind('<Return>', send)

def receive():
    global uses
    while True:
        data = s.recv(1024)
        data = data.decode()
        print("rec_data:", data)
        try:
            uses = json.loads(data)
            listbox1.delete(0, tkinter.END)
            listbox1.insert(tkinter.END, "当前在线用户:")
            for x in range(len(uses)):
                listbox1.insert(tkinter.END, uses[x])
            users.append('------Group chat-------')
        except:
            data = data.split('~')
            print("data_after_slpit:",data) #data_after_slpit: ['cccc', 'a', '0/1']
            userName = data[0]   #data
            userName = userName[1:]
            message = data[1]  #name
            chatwith = data[2]  #destination
            message = '  ' + message + '\n'
            recv_time = " "+userName+"   "+time.strftime ("%Y-%m-%d %H:%M:%S", time.localtime()) + ': ' + '\n'
            listbox.tag_config('tag3', foreground='green')
            listbox.tag_config('tag4', foreground='blue')
            if chatwith == '0':  # 群聊
                listbox.insert(tkinter.END, recv_time, 'tag3')
                listbox.insert(tkinter.END, message)
            elif chatwith != '0':  # 私聊别人或是自己发出去的私聊
                if userName == user:                     #如果是自己发出去的,用私聊字体显示
                    listbox.insert(tkinter.END, recv_time, 'tag3')
                    listbox.insert(tkinter.END, message, 'tag4')
                if chatwith == user:                                    #如果是发给自己的，用绿色字体显示
                    listbox.insert(tkinter.END, recv_time, 'tag3')
                    listbox.insert(tkinter.END, message, 'tag4')

            listbox.see(tkinter.END)


r = threading.Thread(target=receive)
r.start()  # 开始线程接收信息

window2.mainloop()
s.close()
