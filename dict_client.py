from socket import *


def login2():
    s.send("注册".encode())
    data = s.recv(1024).decode()
    if data = 'OK':
        while True:
            name = str(input("请输入用户名"))
            s.send(name.encode())
            data = s.recv(1024).decode()
            if data = 'name is already exist':
                print("用户名重复,请重新输入")
                continue
            else:
                while True:
                    try:
                        password = str(input("请输入密码"))
                        s.send(bytes(password,'utf-8'))
                        password = str(input("请再次输入密码"))
                        s.send(bytes(password,'utf-8'))
                        data = s.recv(1024).decode()
                        if data = 'password is not same Please enter twice':
                            print("两次密码不一致,请重新输入")
                            continue
                        else:
                            print("注册成功")
                            return
                    except Exception as e:
                        print(e)
def main():
    str1 = '''1.登录
2.注册
3.退出
    '''
    #!/usr/bin/env python3
    ip = argv[1]
    port = argv[2]
    addr = (ip,port)
    s = socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.connect(addr)
    print(str1)
    a = int(input('请选择'))
    if a == 1:
        s.send("登陆".encode())
    elif a == 2:
        login()
        print(str1)
    
if __name__ == "__main__":
    main()