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
            data['host'] = info[2]
            data['name'] = info[0]
            data['upstream'] = info[1]
            data['uuid'] = uuid.uuid4()
            data_dict[data['host']] = data
        return data_dict
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

def Modify_upstream():
    pass


if __name__ == '__main__':
    f1  = 'upstream_info.txt'
    f2 = 'conf/nginx.conf'
    up_name = 'p2p_oms'
    #print upstream_format(f1)

    #for i in Match_upstream(f2,up_name):
    #    print i,
    dist = Match_upstream(up_name,f2)
    for i in sorted(dist):
        print dist[i],
