#coding=utf-8
__author__ = 'houkl'
import uuid
import re
data_dict={}
def upstream_format(f1='upstream_info.txt'):
    #格式化upstream_info.txt 文本内容，add uuid 以便以后入库字符码唯一
    global data_dict
    with file(f1,'r') as f:
        for i in [i for i in f.readlines()]:
            data = {}
            info = i.split()
            if info:
                data['host'] = info[2]
                data['name'] = info[0]
                data['upstream'] = info[1]
                data['uuid'] = uuid.uuid4()
                data_dict[data['host']] = data
        return data_dict
        pass

def Nginx_dist(ngf):
    #将nginx.conf 处理成字典，以行号为k，行内容为值
    nginx_dist = {}
    with file(ngf,'r') as f:
        nginx_conf = (i for i in f.readlines())
        L_num = 0
        for L in nginx_conf:
            nginx_dist[L_num] = L
            L_num += 1
    return nginx_dist
    pass
def Match_upstream(up_name,nginx_f):
    #匹配nginx.conf 中的upstream段落,返回以{[行号-1]:行内容} 形式的字典upstm_dist
    upstm_dist = {}
    with file(nginx_f,'r') as f:
        re_upstart = re.compile(r'''%s .*\{''' % up_name)
        re_upend = re.compile(r'\s*\}$')
        nginx_conf = (i for i in f.readlines())
        L_num = 0
        for L in nginx_conf:
            if re_upstart.findall(L):
                upstm_dist[L_num] = L
                L_num +=1
                for L1 in nginx_conf:
                    if re_upend.findall(L1):
                        upstm_dist[L_num] = L1
                        return upstm_dist
                    upstm_dist[L_num] = L1
                    L_num +=1
            L_num +=1

if __name__ == '__main__':
    upstream_format()