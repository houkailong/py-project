#coding=utf-8
__author__ = 'houkl'
import upstream
import re
import shutil
import log,logging
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
                self.upstream = self.info[a[1]]['upstream']
                return self.upstream
        else:
            print u'%s 不符合要求' % num

    def Ser_upstm(self,ups_name,ng_conf):
        self.upstm_dist = upstream.Match_upstream(ups_name,ng_conf)
        # 定义一个按顺序显示server 信息的字典
        self.ser_dist = {}
        n = 1
        for i in sorted(self.upstm_dist):
            ser = re.compile(r'\s*server ')
            if ser.findall(self.upstm_dist[i]):
                ser_list = re.split('\s+|;',self.upstm_dist[i])
                ser_list[0] = '\t\t'
                ser_list[len(ser_list)-1] = '\n'
                self.ser_dist[n] = ser_list
                n += 1
        return self.ser_dist

    def Show_ser(self):
        print '*' * 40
        print u'\033[1;31;mupstream名字：%s\033[0m' % self.upstream
        for k,v in self.ser_dist.items():
            if 'down' in v:
                print '%s.%s \033[1;32;m[%s]\033[0m' % (k,v[2].split(':')[0],'down')
            else:
                print '%s.%s \033[1;32;m[%s]\033[0m' % (k,v[2].split(':')[0],'up')
        print '*' * 40 + '\n'
        pass

    def Log_w(self,upstm,server,status):
        if status == 'down;':
            sta = 'down'
        elif status == ';':
            sta = 'up'
        else:
            pass
        log_info = '%s\t%s\t%s' % (upstm,server,sta)
        logging.info(log_info)
        pass

    def __Modify_ser(self,ser_list,req='up'):
        '''
        供Modify_ser 函数调整服务器状态使用
        :param ser_list: upstream中server的list 格式
        :param req: 要达到的一个需求：'up'表示上线，'down'表示下线
        :return: 达到需求后的server list 结果
        '''
        if req == 'up':
            if 'down' in ser_list:
                ser_list[ser_list.index('down')] = ';'
            else:
                ser_list[ser_list.index('')] = ';'
        elif req == 'down':
            if 'down' in ser_list:
                ser_list[ser_list.index('down')] = 'down;'
            else:
                ser_list[ser_list.index('')] = 'down;'
        else:
            pass
        ser_list[0] = '\t\t\t'
        return ser_list
        pass

    def Modify_ser(self,upstm,ser_num):
        ser_num_list = [int(x) for x in ser_num.split()]
        for i,v in self.ser_dist.items():
            if i in ser_num_list:
                req = 'up'
                v1 = self.__Modify_ser(v,req)
                #.join 是将list转化成字符串
                ser =' '.join(v1)
                ser_fat = re.split('\s+|\n',ser)
                #self.Log_w(upstm,ser_fat[2],ser_fat[3])
            else:
                req = 'down'
                v1 = self.__Modify_ser(v,req)
                ser = ' '.join(v1)
                ser_fat = re.split('\s+|\n',ser)
                #self.Log_w(upstm,ser_fat[2],ser_fat[3])
            if ';' in ser_fat:
                result = ';'
            else:
                result = 'down;'
            self.Log_w(upstm,ser_fat[2],result)

            #此处开始修改upstream 段内容
            for m,k in self.upstm_dist.items():
                if v[2] in k:
                    self.upstm_dist[m] = ser
        pass

    def Modify_nginx(self,ngf):
        #修改nginx upstream 主机内容
        self.nginx_dist = upstream.Nginx_dist(ngf)
        for k in sorted(self.upstm_dist):
            self.nginx_dist[k] = self.upstm_dist[k]
        return self.nginx_dist
        pass
    def Write_nginx(self,ngf_n):
        #将更新后的内容生成到新的文件
        with file(ngf_n,'wb') as fn:
            Ln = (self.nginx_dist[L] for L in sorted(self.nginx_dist))
            for l in Ln:
                fn.write(l)
        pass

if __name__ == '__main__':
    f1 = 'conf/nginx.conf1'
    f2 = 'conf/nginx.conf2'
    upstream_nginx = Upstream_Nginx()
    item=upstream_nginx.Choice_item()
    for a in [i for i in item]:
        print a[0],a[1]
    Item_num = raw_input(u'请输入项目序号：')
    ups_name = upstream_nginx.Find_upstm(Item_num)
    ser_upstm = upstream_nginx.Ser_upstm(ups_name,f1)
    #显示server 状态
    upstream_nginx.Show_ser()
    #ser_num = int(raw_input(u'请输入提供服务的服务器编号：'))
    ser_num = raw_input(u'请输入提供服务的服务器编号：')
    #while not ser_upstm.has_key(ser_num):
    #    ser_num = int(raw_input(u'请输入提供服务的服务器编号：'))
    upstream_nginx.Modify_ser(ser_num)
    upstream_nginx.Modify_nginx(f1)
    #新建nginx.conf 配置文件
    upstream_nginx.Write_nginx(f2)
    #替换原文件
    shutil.move(f2,f1)
    #显示修改后的upstream 结果
    ups_name = upstream_nginx.Find_upstm(Item_num)
    ser_upstm = upstream_nginx.Ser_upstm(ups_name,f1)
    upstream_nginx.Show_ser()


