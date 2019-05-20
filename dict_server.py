from socket import *
from multiprocessing import Process
from pymysql import *


def login():
    c.send(b'Please input your message')

def handle():
    data = c.recv(1024).decode()
    if data = "注册":
        login()






def main():
    addr = ('0.0.0.0',8888)
    s = socket()
    s.bind((addr))
    s.listen(5)
    while True:
        try:
            c,addr = s.accept()
        except:
            print("请重新连接")
            continue
        p = Process(target = handle)
        p.start()
        p.Daemon = True