import socket
import os
import json
import sys

ERROR = {'101': '无效指令',
        '102': '账号已存在',
        '103':'账号不存在，或密码错误',
        '444':'未知错误'
         }
class Ftp_client():
    def __init__(self):
        self.client=socket.socket()
        self.client.connect(('localhost',9999))
        self.original_cmd = {'adduser': '注册新用户',
                       'login': '登录FTP账号',
                        'exitftp': '退出FTP'
                           }
        self.original_txet = '请输入指令代码:'
        self.__login()
    def __login(self):
        self.txet= self.original_txet
        self.usable_cmd=self.original_cmd
        while True:
            order=input(self.txet).strip().split()
            if not len(order):
                continue
            if order[0] not in self.usable_cmd:
                print('无法执行该命令，请先注册或登录账号')
                continue
            data = {'cmd': order}
            if order[0]=='logout' or order[0]=='exitftp':
                func=getattr(Ftp_client,order[0])
                func(self,data)
                continue
            self.client.send(json.dumps(data).encode())
            res=self.client.recv(1024).decode('utf-8')
            result=json.loads(res)
            if result['result']:
                if hasattr(Ftp_client,result['cmd']):
                    func=getattr(Ftp_client,result['cmd'])
                    func(self,result)
                else:
                    print(result['msg'])
            else:
                print(result['reason'])
    def response(self,resdata):
        order=input(resdata['msg'])
        self.client.send(order.encode())
    def activate(self,resdata):#激活登录状态，获取可使用命令
        self.usable_cmd=resdata['usablecmd']
        self.txet=resdata['homepath']+'>>'#改变输入提示符
    def logout(self,data):#发送退出请求
        self.client.send(json.dumps(data).encode())
        res=json.loads(self.client.recv(1024).decode())
        if res['result']:
            self.usable_cmd=res['usablecmd']
            self.txet= self.original_txet
    def exitftp(self,data):
        self.client.send(json.dumps(data).encode())
        self.client.close()
        sys.exit()




a=Ftp_client()
# print(hasattr(Ftp_client,'activate'))