#!/bin/sh
date=`date +%Y%m%d`
today=`date +%s`
updatetime=`date +%Y-%m-%d-%H:%M`
vertime=`date +%Y-%m-%d`
dir="/home/deploy_Package/RELEASE-ops"
rsync="rsync -avz --progress --partial --delete --exclude-from "/home/syspub/bin/app/git""
logdir=/home/syspub/log

[ ! -s packageName ] && exit
> ~/log/update-all

for i in `cat packageName`
do 

result=`curl -d "param=$i" "http://update.haodaibao.com:9527/decompress.php" 2> /dev/null`
res=`echo "$result" | awk -F '@' '{print $1}'`
tomcatName=`echo "$result" | awk -F '@' '{print $2}'`

[ -z $tomcatName ] && exit


if [ "$res" = "ok" ]
   then
          
           $rsync -e 'ssh -p 21222' root@update.haodaibao.com:$dir/$tomcatName /apps/ > $logdir/$tomcatName-add.log
           delet1=`grep "deleting" $logdir/$tomcatName-add.log`
           if [ -n "$delet1" ]
              delet=`grep "deleting" $logdir/$tomcatName-add.log |awk -F"deleting " '{print $2}'`
             then
                for ii in $delet
                do
                        cd /apps/$tomcatName && git rm /apps/$ii
                done
           fi

           q=`grep "$tomcatName/[a-zA-Z0-9]" $logdir/$tomcatName-add.log|grep -v "/$"  |wc -l`
           if [ $q = 0 ] ;then 
                echo "$tomcatName no update !!!!!"
                else
                cd /apps/$tomcatName && git add . && git commit -m "$vertime.$v" &> /dev/null && git push origin master 2> /dev/null
                cd 
                for i in `cat /home/syspub/bin/app/applist`;do echo $i|grep $tomcatName |awk -F. '{print $1}';done >> ~/log/update-all
          fi
          echo -e """
[ \033[32m --- $tomcatName --- \033[0m ]
`grep "$tomcatName/[a-zA-Z0-9]" $logdir/$tomcatName-add.log |grep -v "/$"`
	  """
   else
        
    echo -e """
[ \032[32m --- $tomcatName --- \033[0m ]
echo '调用解压程序出错，退出！'
        """
    exit 1
fi


done

[ -s ~/log/update-all ] && echo "上线序号："`cat ~/log/update-all`

