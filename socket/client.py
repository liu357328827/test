import socket
client=socket.socket()
client.connect(('127.0.0.1',9999))
# msg=input('>>').encode('utf-8')
msg=r'G:\123\新建文本文档.txt'.encode('utf-8')
client.send(msg)
rusult=client.recv(1024).decode()
if rusult.isnumeric():
    print('进入下载程序')
    file=r'G:\123\新建文本文档(2).txt'
    f=open(file,'wb')
    file_size=int(rusult)
    get_file_size=0
    file_text=b''
    while get_file_size<file_size:
        temp=client.recv(1024)
        print(temp)
        get_file_size+=len(temp)
        file_text+=temp
        f.write(temp)
    else:
        f.close()
        print('下载完成！')