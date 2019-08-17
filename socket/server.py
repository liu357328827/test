import socket
import os
sever=socket.socket()
sever.bind(('0.0.0.0',9999))
sever.listen()
while True:
    print('等待请求')
    conn,addr=sever.accept()
    print(addr,'发来请求')
    while True:
        file_path=conn.recv(1024).decode()
        print(file_path,type(file_path))
        if not file_path:
            print(addr,'断开了连接')
            break
        if os.path.isfile(file_path):
            print("1")
            file_size=os.stat(file_path).st_size
            conn.send(str(file_size).encode())
            print(2)
            f=open(r'G:\123\新建文本文档.txt','rb')
            print(r"G:\123\新建文本文档.txt 打开了")
            for line in f:
                print(line)
                conn.send(line)
        else:
            print('2')
            conn.send('文件不存在'.encode('utf-8'))