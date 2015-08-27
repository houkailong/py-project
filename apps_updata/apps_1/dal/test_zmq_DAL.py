# encoding=UTF-8
__author__ = 'xuebaoku'
import json

import conf


class ZMQ_DAL():
    def __init__(self,data,logs):
        from apps_1.API_2 import HttpNetRobot
        self.data = data
        self.logs = logs
        self.Http = HttpNetRobot('http://%s:%s/'%(conf.Url_ip, conf.Url_post),self.logs)
        pass
    def Inquire(self,msg):
        """
        开始执行查询
        :param msg:
        :return:
        """
        self.logs.info('开始执行查询')
        try:
            #Package = self.Http.get('api/inquire/Package/uuid/%s/'%(msg['Package']['uuid']))
            Project = self.Http.get('api/inquire/Project/uuid/%s/'%(msg['Project']['uuid']))
            #assert Package
            assert Project
            self.logs.info("Package:")
            #for i,v in Package.items():
            #    self.logs.info("%s:%s"%(i,v))
            self.logs.info("Project:")
            for i,v in Project.items():
                self.logs.info("%s:%s"%(i,v))
        except Exception as e :
            data={'mode':False,'data':{'message':'查询失败\n%s'%e.message}}
            return data
        data={'mode':True,'data':{'message':'参数执行成功,返回查询结果','msg':{'Project':{"status":Project['status']}}}}
        return data
    def __http_package(self,msg):
        try:
            post_data = {
                    "caption": msg['caption'],
                    "Pull_user": msg['Pull_user'],
                    "Pull_port": msg['Pull_port'],
                    "Pull_server": msg['Pull_server'],
                    "Pull_path": msg['Pull_path'],
                    "code": 'unknown',
                }
        except Exception as e :
            return (False,'获取Package信息失败!请重试\n%s'%e.message)
        http,data = self.Http.send('api/Package/',post_data=post_data)
        if http:
            return (True,data)
        else:
            return (False,data)
    def __val_OPTIONS(self,data,val):
        for i in data:
            if val == i['display_name']:
                return i['value']
        return False
    def __http_Project(self,msg):
        try:
            http , OPTIONS = self.Http.OPTIONS('api/Task/')
            assert http
            OPTIONS = OPTIONS['actions']['POST']
        except Exception as e :
            return (False,'获取OPTIONS失败.%s'%e.message)
        try:
            msg['Project']['Duct'] = self.__val_OPTIONS(data=OPTIONS['Duct']['choices'],val=msg['Project']['Duct'])
            assert msg['Project']['Duct']
        except Exception as e :
            return (False,'获取Duct失败.%s'%e.message)
        try:
            task_type = msg['Project']['task_type']
        except :
            task_type = 1
        try:
            execute_type = self.__val_OPTIONS(data=OPTIONS['execute_type']['choices'],val=msg['mode'])
            assert execute_type
        except :
            execute_type = 0
        try:
            post_data = {
                    "task_type": task_type,
                    "execute_type": execute_type,
                    "name": msg['Project']['name'],
                    "content":  msg['Project']['message'],
                    "is_template": False,
                    "description": msg['Project']['message'],
                    "status": 'unknown',
                    "package": int(msg['Package']['id']),
                    "Duct": int(msg['Project']['Duct']),
                    "created_by": 2
                }
        except Exception as e :
            return (False,'获取package信息失败!请重试\n%s'%e.message)
        self.logs.info("post_data:\n")
        for i,v in post_data.items():
            self.logs.info("%s:%s"%(i,v))
        http,data = self.Http.send('api/Task/',post_data=post_data)
        if http:
            return (True,data)
        else:
            return (False,data)
    def onlinegray(self,msg):
        """
        上线灰度
        :param msg:
        :return:
        """
        self.logs.info('上线灰度')
        #录入包信息
        Package = self.__http_package(msg['Package'])
        self.logs.info(json.dumps(Package))
        if not Package[0]:
            data={'mode':False,'data':{'message':'录入包信息失败\n%s'%Package[1]}}
            return data
        else:
            Package = Package[1]
            del msg['Package']
            msg['Package'] = {'uuid':Package['uuid'],'id':Package['url'].split('/')[-2]}
        self.logs.info(json.dumps(msg['Package']))
        #录入线上信息
        Project = self.__http_Project(msg)
        self.logs.info(json.dumps(Project))
        if not Project[0]:
            data={'mode':False,'data':{'message':'录入上线息失败\n%s'%Project[1]}}
            self.Http.DELETE(Package['url'])
            return data
        else:
            del msg['Project']
            Project = Project[1]
            msg['Project'] = {'uuid':Project['uuid'],'id':Project['url'].split('/')[-2]}
        self.Forcibly_Project(msg)
        data={'mode':True,'data':{'message':'更新信息成功,并发布强制重启命令','msg':msg}}
        return data
    def __http_Put(self,msg,Package):
        #获取线上详细信息
        try:
            OPTIONS = self.Http.get('api/inquire/Project/uuid/%s/'%(msg['Project']['uuid']))
            assert OPTIONS
            self.logs.info("OPTIONS:\n")
            for i,v in OPTIONS.items():
                self.logs.info("%s:%s"%(i,v))
        except Exception as e :
            return (False,'获取信息失败\n%s'%e.message)
        #修改线上信息
        try:
            post_data = {
                    "task_type":  OPTIONS['task_type'],
                    "execute_type":  OPTIONS['execute_type'],
                    "name":  OPTIONS['name'],
                    "content":   OPTIONS['content'],
                    "is_template":  OPTIONS['is_template'],
                    "description": OPTIONS['description'],
                    "status": OPTIONS['status'],
                    "package": int(Package['url'].split('/')[-2]),
                    "Duct": int(OPTIONS['Duct_id']),
                    "created_by": OPTIONS['created_by_id']
                }
            http,data  = self.Http.PUT('api/Task/%s/'%(OPTIONS['id']),post_data)
            assert http
            self.logs.info("PUT:\n")
            for i,v in OPTIONS.items():
                self.logs.info("%s:%s"%(i,v))
            return (True,OPTIONS)
        except Exception as e :
            return (False,'修改信息失败 \n%s'%e.message)

    def Forcibly_Project(self,msg):
        self.logs.info('开始强制重启')
        self.data.put(msg)
        data={'mode':True,'data':{'message':'参数执行成功'}}
        return data

def test():
    pass


if __name__ == '__main__':
    test()