from socket import *
from multiprocessing import Process
from pymysql import *
import sys
import signal

def login(c,db,cur):
    c.send(b'OK')
    try:
        # db = connect( host="localhost",user="root",
        # password="123456",database="login",
        # charset="utf8")
        # cur = db.cursor()
        cur.execute('select name from login1')
        t = cur.fetchall()
        l1 = list(t)
        l2 = []
        for i in l1:
            l2.append(i[0])
        while True:
            name = c.recv(1024).decode()
            if not name:
                sys.exit("注册失败")
            if l2 == []:
                c.send(b'name is available,Please enter your password')
            else:
                for i in l2:
                    if i == name:
                        c.send(b'name is already exist')
                        continue
            c.send(b'name is available,Please enter your password')
            while True:
                l4 = []
                for i in range(2):
                    password = c.recv(1024).decode()
                    l4.append(password)
                if l4[0] != l4[1]:
                    c.send(b"password is not same Please enter twice")
                    continue
                else:
                    c.send(b'successfully login')
                    cur.execute('insert into login1(name,password) \
                                values(%s,%s);',[name,l4[0]])
                    db.commit()
                    print(name,"用户注册成功")
                    return
    except Exception as e:
        print(e)
def enter(c,cur):
    c.send(b"OK")
    cur.execute('select name from login1')
    t = cur.fetchall()
    l1 = list(t)
    l2 = []
    for i in l1:
        l2.append(i[0])
    while True:
        name = c.recv(1024).decode()
            if not name:
                sys.exit("注册失败")
            if l2 = []:
                c.send(b'Please login first')     
def handle(c,db1,cur1):
    try:
        db1 = connect( host="localhost",user="root",
                    password="123456",database="login",
                    charset="utf8")
        cur1 = db1.cursor()
        data = c.recv(1024).decode()
        if data == "注册":
            login(c,db1,cur1)
        if data == "quit":
            print("用户退出")
        if data = "登录":
            enter(c)
    finally:
        cur1.close()
        db1.close()


def main():
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)
    addr = ('0.0.0.0',8888)
    s = socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(addr)
    s.listen(5)
    while True:
        try:
            c,addr = s.accept()
        except:
            print("请重新连接")
            continue
        p = Process(target = handle,args = (c,))
        p.daemon = True
        p.start()

if __name__ == "__main__":
    main()