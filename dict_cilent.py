from socket import *











def main():
    #!/usr/bin/env python3
    ip = argv[1]
    port = argv[2]
    addr = (ip,port)
    s = socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.connect(addr)
    print(" "*6,end = '')
    print("1.登陆")
    print(" "*6,end = '')
    print("2.注册")
    print("3.退出")
    a = int(input('请选择'))
    if a == 1:
        s.send("登陆".encode())
    elif a == 2:
        s.send("注册".encode())
    
if __name__ == "__main__":
    main()