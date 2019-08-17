import socketserver
import os
import json
import datetime
ERROR = {'101': '无效指令',
        '102': '账号已存在',
        '444':'未知错误'
         }
FTPHOME=r'G:\123\socket\ftp_sever\db\account_data'

original_cmd = {'adduser': '注册新用户',
                       'login': '登录FTP账号',
                        'exitftp': '退出FTP'
                           }
afterologin = {
                 'ls': '显示当前文件夹下所有文件',
                 'pwd': '显示当前所在位置',
                 'cd': '移动到上级目录',
                 'help': '显示帮助文档',
                 'logout': '注销FTP登录账号',
                 'exitftp': '退出FTP',
                 'mkdir':'创建子目录'
                 }
class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            try:
                print('等待接收指令')
                res=self.request.recv(1024).strip()#接收客户端发来的消息
                if not len(res):
                    break
                data = json.loads(res.decode())#解析命令并制作返回数据字典
                if hasattr(MyTCPHandler,data['cmd'][0]):#检测命令有效性e
                    fuc=getattr(MyTCPHandler,data['cmd'][0])
                    fuc(self,data)
                else:
                    data['result']=False
                    data['reason']='无效指令'
                    self.request.send(json.dumps(data).encode())
            except ConnectionResetError as e:
                print(e)
                break
            except ConnectionAbortedError as e:
                print(e)
                break
    def help(self):
        cmd_order = {'add_user id passwd': '注册新用户',
                     'login id passwd': '登录FTP账号',
                     'ls':'显示当前文件夹下所有文件',
                     'pwd':'显示当前所在位置',
                     'cd ..':'移动到上级目录',
                     'help':'显示帮助文档',
                     'logout':'注销FTP登录账号',
                     'exitftp':'退出FTP'
                    }
        self.request.send(json.dumps(cmd_order).encode())
    def adduser(self,data):#创建账号
        id=data['cmd'][1]
        homepath=FTPHOME+'\\'+id
        if os.path.isdir(homepath):
            data['result']=False
            data['reason']='账号已存在'
        else:
            try:
                cdata={'cmd':'response',
                       'result':True,
                       'msg':'请输入密码：'}
                print('cdata',cdata)
                self.request.send(json.dumps(cdata).encode('utf-8'))
                passwd=self.request.recv(1024).decode()
                os.makedirs(homepath)
                userdata=json.dumps({'home':homepath, 'ID':id, 'passwd':passwd})
                with open(homepath+'\%s.json'%id,'w') as f:
                    json.dump(userdata,f)
                data['result'] = True
            except:
                data['result']=False
                data['reason']='未能成功创建家目录'
                self.request.send(json.dumps(data).encode('utf-8'))
    def login(self,data):
        data=self.__authentication(data)
        self.request.send(json.dumps(data).encode())
    def __authentication(self,data):#身份验证
        id = data['cmd'][1]
        passwd = data['cmd'][2]
        homepath = FTPHOME + '\\' + id
        if os.path.exists(homepath):
            with open(homepath+'\%s.json'%id,'r')as f:
                userdata=json.loads(json.load(f))
                if passwd==userdata['passwd']:
                    self.usage_log = {'ID': id,
                                      'home': homepath,
                                      'pwd': homepath,
                                      'usedcmd':[data['cmd']]}
                    print('生成usage_log', self.usage_log)
                    data['result']=True
                    data['cmd']='activate'
                    data['usablecmd']=afterologin
                    data['homepath']=homepath
                else:
                    data['result']= False
                    data['reason']= '密码错误'
        else:
            data['result'] = False
            data['reason'] = '账号不存在'
        return data
    def logout(self,data):#退出登录
        self.usage_log['usedcmd'].append(data['cmd'])
        with open(self.usage_log['home']+r'\operation.log ',"a") as f:
            content=str(datetime.datetime.now())+' %s\n'%self.usage_log['usedcmd']
            f.write(content)
        data['result'] = True
        data['usablecmd'] = original_cmd
        self.request.send(json.dumps(data).encode())
    def exitftp(self,data):#退出FTP
        if hasattr(self,'usage_log'):
            self.logout(data)
        else:
            return
    def pwd(self,data):#显示当前所在位置
        self.usage_log['usedcmd'].append(data['cmd'])
        data['cmd']='pwd'
        data['result']=True
        data['msg']=self.usage_log['pwd']
        self.request.send(json.dumps(data).encode())
    def mkdir(self,data):
        self.usage_log['usedcmd'].append(data['cmd'])
        filepath=self.usage_log['pwd']+'\%s'%data['cmd'][1]
        if os.path.exists(filepath):
            data['result'] = False
            data['reason'] = '该目录已存在'
        else:
            os.makedirs(filepath)
            data['result']=True
            data['cmd']='mkdir'
            data['msg']='创建成功'
        self.request.send(json.dumps(data).encode())
    def cd(self,data):
        self.usage_log['usedcmd'].append(data['cmd'])
        temp=data['cmd'][1].split('\\')
        if temp[0]==self.usage_log['ID']:
            print(self.usage_log['pwd']+'\%s'%temp[0])
            if os.path.exists(self.usage_log['pwd']+'\%s'%temp[0]):
                filepath = self.usage_log['pwd'] + '\%s' % data['cmd'][1]
            else:
                filepath = self.usage_log['home']
                for i in temp[1:]:
                    filepath+='\%s'%i
        else:
            filepath = self.usage_log['pwd'] + '\%s' % data['cmd'][1]
        if os.path.exists(filepath):
            self.usage_log['pwd']=filepath
            data['result'] = True
            data['cmd'] = 'cd'
            data['msg'] = ''
        else:
            data['result'] = False
            data['reason']='该目录不存在'
        self.request.send(json.dumps(data).encode())
    def ls(self,data):
        self.usage_log['usedcmd'].append(data['cmd'])
        msg=os.listdir(self.usage_log['pwd'])
        data['result'] = True
        data['cmd'] = 'ls'
        data['msg'] = msg
        self.request.send(json.dumps(data).encode())







if __name__=='__main__':
    HOST,PORT='localhost',9999
    sever=socketserver.ThreadingTCPServer((HOST,PORT),MyTCPHandler)
    sever.serve_forever()

