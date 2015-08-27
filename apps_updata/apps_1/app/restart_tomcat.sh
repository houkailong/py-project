#!/bin/sh

shdir=`dirname $0`
webpwd=`cd $shdir && pwd`

if [ -n "$1" ]; then
 if [ "$1" = "stop" ]; then
  webpro=`ps aux | grep $webpwd | grep MaxPermSize`
  webpid=`echo $webpro | awk '{print $2}'`
  echo $webpro
  echo $webpid
  kill -9 $webpid
  echo "kill -9 $webpid"
  sleep 1s
  if [ !-n `ps aux | grep $webpwd | grep MaxPermSize` ]; then
   echo "Tomcat stop OK!!!"
  else
   echo "Tomcat stop ERROR!!!"
  fi
 elif [ "$1" = "start" ]; then
  webproo=`ps aux | grep $webpwd | grep MaxPermSize`
  if [ -n "$webproo" ]; then
   echo "Tomcat is runing..."
   echo "$webproo"
   exit;
  fi
  rm -rf $webpwd/work/Catalina
  cd $webpwd/bin
  ./startup.sh
  webprooo=`ps aux | grep $webpwd | grep MaxPermSize`
  webpidd=`echo $webprooo | awk '{print $2}'`
  echo $webprooo
  echo $webpidd
 elif [ "$1" = "restart" ]; then
  sh $0 stop
  sleep 1s
  sh $0 start
 fi
else
 echo "$0 start/stop/restart!"
fi