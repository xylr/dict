from socket import *
from multiprocessing import Process
from pymysql import *
import sys

def login():
    c.send(b'OK')
    try:
        db = connect( host="localhost",user="root",
        password="123456",database="login",
        charset="utf8")
        cur = db.cursor()
        cur.excute('select name from login1')
        t = cur.fetchall()
        l1 = list(t)
        l2 = []
        for i in l1:
            l2.append(i[0])
        
        while True:
            name = c.recv(1024).decode()
            if not name:
                sys.exit("注册失败")
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
                    c.send("password is not same Please enter twice")
                    continue
                else:
                    c.send(b'successfully login')
                    cur.excute('insert into login1('name','password') \
                        values(%s%s);',[name,l4[0]])
                    db.commit()
                    return
    except Exception as e:
        print(e)
    finally:
        cur.close()
        db.close()
def handle():
    data = c.recv(1024).decode()
    if data = "注册":
        login()






def main():
    addr = ('0.0.0.0',8888)
    s = socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
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

if __name__ == "__main__":
    main()