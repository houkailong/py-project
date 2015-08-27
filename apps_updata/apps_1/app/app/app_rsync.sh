#!/bin/sh
name=name
date=`date +%Y%m%d`
today=`date +%s`
updatetime=`date +%Y-%m-%d-%H:%M`
vertime=`date +%Y-%m-%d`


status(){
for app in `cat applist`
do
 echo $app|awk -F. '{print $NF}'
done
}

logdir=/home/syspub/log
for i in `status`
do 

rsync -avz --progress --partial --delete --exclude-from "/home/syspub/bin/app/git" -e 'ssh -p 22222' deploy@update.haodaibao.com:/home/deploy/tomcat/apps/$i /apps/ > $logdir/$i-add.log 
delet1=`grep "deleting" $logdir/$i-add.log`
        if [ -n "$delet1" ]
delet=`grep "deleting" $logdir/$i-add.log |awk -F"deleting " '{print $2}'`

         then
                for ii in $delet
                do
                        cd /apps/$i && git rm /apps/$ii
                done
        fi

q=`grep "$i/[a-zA-Z0-9]" $logdir/$i-add.log |wc -l`

        if [ $q = 0 ] ;then 
                echo "$i no update !!!!!"
                else
                cd /apps/$i && git add .
                cd /apps/$i && git commit -m "$vertime.$v"
                cd /apps/$i && git push origin master
                cd 
        fi
done
