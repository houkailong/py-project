for i in `cat packageName`
do
echo $i
result=`curl -d "param=$i" "http://update.haodaibao.com:9527/decompress.php" 2> /dev/null`
res=`echo "$result" | awk -F '@' '{print $1}'`
tomcatName=`echo "$result" | awk -F '@' '{print $2}'`

echo "res:$res"
echo "tomcatName:$tomcatName"
done
