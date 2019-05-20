from socket import *
from multiprocessing import Process
from pymysql import *
import sys
import signal

def login(c,db,cur):
    c.send(b'OK')
    try:#查询login1表中的用户注册信息
        cur.execute('select name from login1')
        #拿到所有的用户姓名
        t = cur.fetchall()
        #将拿到的元组转换为列表方便进行增删改查
        l1 = list(t)
        l2 = []
        #将所有的姓名加入到新列表方便进行姓名的是否重复查询
        for i in l1:
            l2.append(i[0])
        while True:
            #循环接收用户名,并判断是否重复
            name = c.recv(1024).decode()
            if not name:
                sys.exit("注册失败")
            if l2 == []:
                c.send(b'name is available,Please enter your password')
            else:
                for i in l2:
                    #若用户名存在则重新进行用户名注册
                    if i == name:
                        c.send(b'name is already exist')
                        continue
            c.send(b'name is available,Please enter your password')
            while True:
                #用l4列表来判断两次接收到的密码是否一致
                l4 = []
                for i in range(2):
                    password = c.recv(1024).decode()
                    l4.append(password)
                if l4[0] != l4[1]:
                    #密码不相同则重新输入
                    c.send(b"password is not same Please enter twice")
                    continue
                else:#密码相同将用户信息插入到用户信息表
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
    #将姓名和密码一起查出来
    cur.execute('select name,password from login1')
    #存入元组并强转为列表方便增删改查
    t = cur.fetchall()
    l1 = list(t)
    l2 = []
    for i in l1:
        l2.append(i[0])
    while True:
        #接收用户名
        name = c.recv(1024).decode()
        if not name:
            sys.exit("登录失败")
        if l2 == []:
            c.send(b'Please login first')
            return
        else:
            if name in l2:
                c.send(b"name is right")
                break
            else:
                c.send(b'name is not exist,please input again')
    while True:
        #根据用户名匹配相对应的密码进行和客户端的密码校对
        cur.execute('select password from login1 where name = %s',[name])
        t = cur.fetchone()
        password = c.recv(1024).decode()
        if not password:
            sys.exit("登录失败")
        if t[0] == password:
            c.send(b"Successfully enter")
            return name
        if t[0] != password:
            c.send(b'password is wrong please input again')
def handle(c):
    try:#连接用户信息数据库,进行相应的操作
        db1 = connect( host="localhost",user="root",
                    password="123456",database="login",
                    charset="utf8")
        #创建cur1对象来操作数据库
        cur1 = db1.cursor()
        #连接历史记录表,进行历史记录的读取
        db2 = connect( host="localhost",user="root",
                    password="123456",database="login",
                    charset="utf8")
        cur2 = db2.cursor()
        #接收用户发送的请求
        data = c.recv(1024).decode()
        if data == "注册":
            login(c,db1,cur1)
        if data == "quit":
            print("用户退出")
        if data == "登录":
            name = enter(c,cur1)
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
        #创建子进程接收客户端请求,主进程接收客户端连接
        p = Process(target = handle,args = (c,))
        p.daemon = True
        p.start()

if __name__ == "__main__":
    main()