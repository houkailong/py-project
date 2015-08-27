#!bin/bash
DIR=/home/syspub/bin/app
D=`date +%Y%m%d%H%M%S`
updatetime=`date +%Y-%m-%d-%H-%M`
time_baek()
{
clear
subject="欢迎使用好贷宝自动化上线系统！"
time=`date "+%Y-%m-%d %T"`
vertime=`date +%Y.%m.%d`
echo "
       日期:$time
       ==============================
        $subject
       ==============================
       选择业务："
cat applist
}

while [ ture ]
do
a[1]="tomcat-hde_online"              
a[2]="tomcat-hde_oms"         
a[3]="tomcat-jdy_online"               
a[4]="tomcat-jdy_oms"            
a[5]="tomcat-userService"            
a[6]="tomcat-bankserver"            
a[7]="tomcat-passport"            
a[8]="tomcat-ROOT"            
a[9]="tomcat-pay_biz"
a[10]="tomcat-pay_bank"
a[11]="tomcat-pay_settle"
a[12]="tomcat-pay_ppms"
a[13]="tomcat-pay_auth"
a[14]="tomcat-purse-member"            
a[15]="tomcat-purse-account"        
a[16]="tomcat-purse-web"
a[17]="tomcat-zrj-base-service"     
a[18]="tomcat-qb-admin"
a[19]="tomcat-qb-auth"
a[20]="tomcat-qb-sso"

time_baek
echo -n "
警告：更新文件了吗？（sh app_rsync.sh ）
请输入要更新的业务："
        read tepy
echo -n "请输入要更新的批次（内测输入1、生产首批输入2、生产次批输入3）："
        read tepy2
tepy3='$4'
echo -n "默认更新,回滚输入(rollback):"
        read rollback
if [ "$rollback" = "rollback" ]
   then
        ls $DIR/log-update/ |tail -3
        echo -n "选择日期:"
        read rtiem
        if [ -n $rtiem ]
        then
          grep "^$tepy2" $DIR/log-update/$rtiem|tail -3
          echo -n "选择版本号:"
          read id

          for i in $tepy
          do
                  ip=`awk "/^${a[$i]} $tepy2 / {print $tepy3}" ip_list `
                  code=`echo "${a[$i]}" |awk -F"tomcat-" '{print $NF}'`
                  for ii in $ip
                  do
                  echo ""
                  echo -e "\033[32;49;1m -------------- $ii ------------------------ \033[39;49;0m"
                  echo ""
                  ssh -t deploy@$ii ". .bashrc && sudo su - appuser -c \"/apps/${a[$i]}/bin/shutdown.sh"\"
                  ssh -t deploy@$ii "cd /apps/${a[$i]}/webapps/$code && /usr/bin/git reset --hard  \`git reflog |awk '{if(\$NF==\"$id\")print \$1}'\`"  
                  ssh -t deploy@$ii ". .bashrc && sudo su - appuser -c /apps/${a[$i]}/bin/startup.sh" 
                  done &
          done 
          exit
        else
          echo -n "请输入日期!!!!"
          exit
        fi
    else
        if [ ! -f "$DIR/log-update/$vertime" ]; then 
                touch $DIR/log-update/$vertime
        fi
        version=`awk -F"-" '{if($1=='$tepy2')print $3}' $DIR/log-update/$vertime |tail -1 `
        v=`expr $version + 1`
        echo "$tepy2-$vertime-$v" >> $DIR/log-update/$vertime
        for i in $tepy
        do
                ip=`awk "/^${a[$i]} $tepy2 / {print $tepy3}" ip_list `
                for ii in $ip
                do
                code=`echo "${a[$i]}" |awk -F"tomcat-" '{print $NF}'`
                echo ""
                echo -e "\033[32;49;1m -------------- $ii ------------------------ \033[39;49;0m"
                echo ""
                ssh -t deploy@$ii ". .bashrc && sudo su - appuser -c \"/apps/${a[$i]}/bin/shutdown.sh"\"
                #ssh -t deploy@$ii "rm -rf /apps/${a[$i]}/webapps/$code && mkdir -p /apps/${a[$i]}/webapps/"
                #ssh -t deploy@$ii ". .bashrc && cd /apps/${a[$i]}/webapps/ && sh ./git.sh"
                #ssh -t deploy@$ii "cd /apps/${a[$i]}/webapps/$code && /usr/bin/git pull origin master >> /apps/gitlog/$tepy2-$vertime-$v && /usr/bin/git add . && /usr/bin/git commit -m \"$tepy2-$vertime-$v\""
 #               #ssh -t deploy@$ii ". .bashrc && sudo su - appuser -c /apps/${a[$i]}/bin/startup.sh"
                done
        done
        exit
fi
done
