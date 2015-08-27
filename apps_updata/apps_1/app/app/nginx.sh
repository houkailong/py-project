#!bin/bash
conf=/apps/tengine/conf/nginx.conf
confdir=/home/syspub/bin/app/log-nginx
tng02=10.19.0.35
tng03=10.19.0.36
date=`date +%Y%m%d:%H%M%S`

test(){
    for i in `awk '{if($NF=="'$1'") print $2"-"$3}' $confdir/nginx.conf`
       do 
	    if [[ `echo $i |awk -F- '{print $2}'` == "down" ]]
	       then
	          echo -e "`echo $i |awk -F- '{print $1}'`[\033[31m down \033[0m] "
	       else
	           echo -e "`echo $i |awk -F- '{print $1}'`[ \033[32m up \033[0m ] "
	    fi
   done 

}

status(){
for app in `cat applist`
do
 echo $app
 test "#`echo $app|awk -F. '{print $NF}'`"
 echo ""
done
}

while [ ture ]
do
a[1]="tomcat-hde_online"                a[23]="tomcat-hdb_mobile"             
a[2]="tomcat-hde_oms"                   a[24]="tomcat-rxb"
a[3]="tomcat-jdy_online"                a[25]="tomcat-hdb_dubbo"
a[4]="tomcat-jdy_oms"                   a[26]="tomcat-rxb_Sales"
a[5]="tomcat-userService"               a[27]="tomcat-trade"
a[6]="tomcat-bankserver"                a[28]="tomcat-member"
a[7]="tomcat-passport"                  a[29]="tomcat-manager"
a[8]="tomcat-ROOT"                      a[30]="tomcat-merchant"
a[9]="tomcat-pay_biz"                   a[31]="tomcat-account" 
a[10]="tomcat-pay_bank"                 a[32]="tomcat-settlement" 
a[11]="tomcat-pay_settle"               a[33]="tomcat-file"
a[12]="tomcat-pay_ppms"                 a[34]="tomcat-weixin"
a[13]="tomcat-pay_auth"                 a[35]="tomcat-hdb_new_job" 
a[14]="tomcat-purse-member"
a[15]="tomcat-purse-account"
a[16]="tomcat-purse-web"
a[17]="tomcat-zrj-base-service"
a[18]="tomcat-qb-admin"
a[19]="tomcat-qb-auth"
a[20]="tomcat-qb-sso"
a[21]="tomcat-hdb_oms"
a[22]="tomcat-hdb_website"

scp deploy@$tng02:$conf $confdir && cp $confdir/nginx.conf $confdir/pull-nginx.conf-$date
status
echo -n "请输入要更新的业务："
        read tepy

echo -n "请输入要更新的批次（生产首批输入2、生产次批输入3）："
        read tepy2
echo -n "请输入操作（up\down）："
        read tepy5
        for i in $tepy
        do
	   tepy3='$4":"$5'
           ip=`awk "/^${a[$i]} $tepy2 / {print $tepy3}" ip_list`
	   if [[ $tepy5 == "up" || $tepy5 == "down" ]]
	       then
                   if [[ $tepy5 == "up" ]]
	              then
		 	 if [[ `grep "#${a[$i]}" $confdir/nginx.conf|grep "$ip"|awk '{print $3}'` == "down" ]]
                            then
				sn=`cat -n $confdir/nginx.conf|sed -n "/#${a[$i]}/{/$ip/p}"|awk '{print $1}'`
				sed -i "$sn s/$ip down/$ip/g" $confdir/nginx.conf
                            else
                               echo $ip ${a[$i]}  is up
			        
                          fi                        
		      else
                          if [[ `grep "#${a[$i]}" $confdir/nginx.conf|grep "$ip"|awk '{print $3}'` != "down" ]]
                            then
			        sn=`cat -n $confdir/nginx.conf|sed -n "/#${a[$i]}/{/$ip/p}"|awk '{print $1}'`
                                sed -i "$sn s/$ip/$ip down/g" $confdir/nginx.conf
                            else
                                echo $ip ${a[$i]}  is down
			  fi
                   fi
           fi
        done
        status
echo -n "请输入操作（n\y:）："
        read tepy6         
        if [[ $tepy6 == "n" || $tepy6 == "y" ]]
           then
             if [[ $tepy6 == "y" ]]
               then
               cp $confdir/nginx.conf $confdir/push-nginx.conf-$date
	       echo "------ $tng02 -------"
               scp $confdir/nginx.conf deploy@$tng02:$conf && ssh deploy@$tng02 "sudo /apps/tengine/sbin/nginx -s reload"
	       echo "------ $tng03 -------"
               scp $confdir/nginx.conf deploy@$tng03:$conf && ssh deploy@$tng02 "sudo /apps/tengine/sbin/nginx -s reload"
               else
                   exit
             fi
               
        fi
        exit

done
