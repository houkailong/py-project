# encoding=UTF-8
__author__ = 'xuebaoku'
import time

#django api
Url_ip = '127.0.0.1'
Url_post = 8000
http_logs_url = True



#日志文件位置
logs_dir = 'logs'
#是否开启特殊报错模式
Error = False
#日志文件.存储地址
logs_file = 'logs/apps_all'
#代码文件.存储地址
data_dir = '/apps/deploy_Package/'
#配置ip地址与端口
IP='127.0.0.1'
PORT=11111
#退出密码
password='123456'
queue_timeout = 5
timeout = 5
rasync = 'rsync -avz --progress --partial --delete --exclude-from '
gitpath_dep='/apps/deploy_Package'
shell_dep='restart.sh'
tempfile = '/tmp/%s.txt'%(time.time())
#配置快速生成.并合并成dict
tomcat_dict={}
#print 'tomca_dictt',tomcat_dict
def  hebin(dict_1):
    global tomcat_dict
    try:
        assert tomcat_dict[dict_1['name']]
    except Exception as e:
        pass
        #print '出现重复错误 %s'%e.message
    tomcat_dict[dict_1['name']] = {'ip':dict_1['ip'],
                                   'path':dict_1['path'],
                                   'port':dict_1['port'],
                                   'shell':dict_1['shell']}


hebin(dict_1={'name':"tomcat-hdb_web",'ip':'127.0.0.1','path':'/apps','port':'8080','shell':'restart.sh','gitpath':'/apps/deploy_Package'})
hebin(dict_1={'name':"tomcat-test01",'ip':'127.0.0.1','path':'/apps','port':'8080','shell':'restart.sh','gitpath':'/apps/deploy_Package'})
#hebin(dict_1={'name':"tomcat-hdb_web",'ip':'127.0.0.1','path':'/apps/','port':'8080','shell':'restart.sh','gitpath':'/apps/deploy_Package'})
if Error:
    print tomcat_dict