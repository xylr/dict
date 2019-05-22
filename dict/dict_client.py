from socket import *
from sys import *
from time import *


def login(s):
    s.send("注册".encode())
    data = s.recv(1024).decode()
    if data == 'OK':
        while True:
            name = str(input("请输入用户名:"))
            s.send(name.encode())
            data = s.recv(1024).decode()
            if data == 'name is already exist':
                print("用户名重复,请重新输入")
                continue
            else:
                while True:
                    try:
                        password = str(input("请输入密码:"))
                        s.send(bytes(password,'utf-8'))
                        password = str(input("请再次输入密码:"))
                        s.send(bytes(password,'utf-8'))
                        data = s.recv(1024).decode()
                        if data == 'password is not same Please enter twice':
                            print("两次密码不一致,请重新输入")
                            continue
                        else:
                            print("注册成功")
                            return
                    except Exception as e:
                        print(e)
def enter(s):
    s.send("登录".encode())
    data = s.recv(1024).decode()
    if data == "OK":
        while True:
            name = str(input("请输入您的用户名:"))
            s.send(name.encode())
            data = s.recv(1024).decode()
            if data == 'Please login first':
                print("请先注册")
                return 'false'
            elif data == "name is not exist,please input again":
                print("用户名错误,请重新输入")
                continue
            else:
                while True:
                    password = input("请输入密码:")
                    s.send(password.encode())
                    data = s.recv(1024).decode()
                    if data == "Successfully enter":
                        print("登陆成功")
                        return "OK"
                    elif data == "password is wrong please input again":
                        print("密码错误,请重新输入")

def check_word(s):
    while True:
        word_name = str(input("请输入所要查询的单词:"))
        s.send(word_name.encode())
        data = s.recv(1024).decode()
        if data == 'Not Found this word':
            print("没有此单词,请重新输入")
            continue
        else:
            print('解释:',data)
            print('''继续查询请输入１         
取消查询请输入任意键

''')
            a = int(input("请问是否要继续查询?"))
            if a == 1:
                continue
            else:
                c.send("退出查询".encode())
                return
def check_history(s):
    str3 = print(""" name    word  date
        """)
    history = s.recv(1024).decode()
    l = history.split("#")
    for i in l:
        print(i)
    return
def main():
    str1 = '''                          1.登录
                          2.注册
                          3.退出
                 请输入对应序号执行相应功能
    '''
    str2 = '''                          1.查单词
                          2.历史记录
                          3.退出到一级界面
                 请输入对应序号执行相应功能
    '''

    #!/usr/bin/env python3
    ip = argv[1]
    port = int(argv[2])
    addr = (ip,port)
    s = socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.connect(addr)
    while True:
        print(str1)
        a = int(input('请选择:'))
        if a == 1:
            message = enter(s)
            if message == "false":
                print(str1)
            elif message == "OK":
                while True:
                    print(str2)
                    a = int(input("请选择:"))
                    if a == 1:
                        s.send("查单词".encode())
                        check_word(s)
                    if a == 2:
                        s.send("查找历史记录".encode())
                        check_history(s)
                    if a == 3:
                        s.send("退出".encode())
                        print("已退回到登录界面")
                        break
        elif a == 2:
            login(s)
            print(str1)
        elif a == 3:
            s.send(b'quit')
            exit("程序退出")
if __name__ == "__main__":
    main()