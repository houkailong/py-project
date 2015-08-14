#coding=utf-8
__author__ = 'houkl'
import upstream
import re
class Upstream_Nginx(object):
    def __init__(self):
        self.info = upstream.upstream_format()

    def Choice_item(self):
        for i,v in self.info.items():
            yield v['name'],i

    def Find_upstm(self,num):
        #查找nginx.conf 中对应的upstream块内容
        re_num = re.compile(r'^%s\.' % num)
        for a in self.Choice_item():
            if re_num.findall(a[0]):
                #通过num 获取域名 a[1],后得到upstream 名字
                upstream = self.info[a[1]]['upstream']
                return upstream

    def Ser_upstm(self,ups_name,ng_conf):
        self.upstm_dist = upstream.Match_upstream(ups_name,ng_conf)
        # 定义一个按顺序显示server 信息的字典
        self.ser_dist = {}
        n = 1
        for i in sorted(self.upstm_dist):
            ser = re.compile(r'\s*server ')
            if ser.findall(self.upstm_dist[i]):
                ser_list = re.split('\s+|;',self.upstm_dist[i])
                self.ser_dist[n] = ser_list
                n += 1
        return self.ser_dist

    def Show_ser(self):
        for k,v in self.ser_dist.items():
            if 'down' in v[3]:
                print '\033[1;31;m%s.%s\033[0m \033[1;32;m[%s]\033[0m' % (k,v[2].split(':')[0],'down')
            else:
                print '\033[1;31;m%s.%s\033[0m \033[1;32;m[%s]\033[0m' % (k,v[2].split(':')[0],'up')
        pass

    def Modify_ser(self,ser_num):
        for i,v in self.ser_dist.items():
            if i == ser_num:
                v[3] = ';'
                #.join 是将list转化成字符串
                ser =' '.join(v)
            else:
                v[4] = 'down;'
                ser = ' '.join(v)
            #此处开始修改upstream 段内容
            for m,k in self.upstm_dist.items():
                if v[2] in k:
                    self.upstm_dist[m] = ser
        print self.upstm_dist
        pass

if __name__ == '__main__':
    f2 = 'conf/nginx.conf'
    upstream_nginx = Upstream_Nginx()
    item=upstream_nginx.Choice_item()
    for a in [i for i in item]:
        print a[0],a[1]
    Item_num = raw_input(u'请输入项目序号：')
    ups_name = upstream_nginx.Find_upstm(Item_num)
    ser_upstm = upstream_nginx.Ser_upstm(ups_name,f2)
    #用于显示server 状态
    upstream_nginx.Show_ser()
    ser_num = int(raw_input(u'请输入提供服务的服务器编号：'))
    while not ser_upstm.has_key(ser_num):
        ser_num = int(raw_input(u'请输入提供服务的服务器编号：'))
    upstream_nginx.Modify_ser(ser_num)


