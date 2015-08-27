#!/bin/sh
name=name
date=`date +%Y%m%d`
today=`date +%s`
updatetime=`date +%Y-%m-%d-%H:%M`
vertime=`date +%Y-%m-%d`


status(){
for app in `cat applist`
do
 #echo $app|awk -F. '{print $1}'
 echo $app|awk -F. '{print $NF}'
done
}

for i in `status`
do 


echo $i
done
