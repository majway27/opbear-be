#echo '{"httpMethod": "POST", "body": "{\"name\": \"test\"}"}' | TABLE_NAME="test.ob.lists" sam local invoke "OBLists"
#echo '{"httpMethod": "GET", "body": "{\"name\": \"test\"}"}' | TABLE_NAME="test.ob.lists" sam local invoke "OBLists"

curl -d '{"uid": "94776f82-5d24-4c24-b042-a1e1690d2290","listid": "5","name":"My List 5"}' http://127.0.0.1:3000/
#curl http://127.0.0.1:3000/