# Get api token 
docker exec -it influxdb influxdb create token --admin

username: my-admin
token: 93ukPnhw6Yrr38ZTd4Ihdj8BgSIVQhb9Xu5bVk3qf7teMdj66gQxuypZB81GhqKaxNn_a02l93437KAYJ6zkAw==


curl -i -X GET http://localhost:8086/health

curl -i -X GET http://localhost:8086/api/v2/buckets \
  -H "Authorization: Token 93ukPnhw6Yrr38ZTd4Ihdj8BgSIVQhb9Xu5bVk3qf7teMdj66gQxuypZB81GhqKaxNn_a02l93437KAYJ6zkAw==" \
  -H "Content-Type: application/json"