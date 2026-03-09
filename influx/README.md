# Get api token 
docker exec -it influxdb influxdb create token --admin

username: my-admin
token: 93ukPnhw6Yrr38ZTd4Ihdj8BgSIVQhb9Xu5bVk3qf7teMdj66gQxuypZB81GhqKaxNn_a02l93437KAYJ6zkAw==


curl -i -X GET http://localhost:8086/health

curl -i -X GET http://localhost:8086/api/v2/buckets \
  -H "Authorization: Token 93ukPnhw6Yrr38ZTd4Ihdj8BgSIVQhb9Xu5bVk3qf7teMdj66gQxuypZB81GhqKaxNn_a02l93437KAYJ6zkAw==" \
  -H "Content-Type: application/json"


url = f"http://localhost:8086"
token = "93ukPnhw6Yrr38ZTd4Ihdj8BgSIVQhb9Xu5bVk3qf7teMdj66gQxuypZB81GhqKaxNn_a02l93437KAYJ6zkAw=="
bucket = "UEdata1"
org = "my-org"
measurement= "UEThroughput"
time_range = "-1h"  


curl --request POST \
"http://localhost:8086/api/v2/query?org=my-org" \
--header "Authorization: Token 93ukPnhw6Yrr38ZTd4Ihdj8BgSIVQhb9Xu5bVk3qf7teMdj66gQxuypZB81GhqKaxNn_a02l93437KAYJ6zkAw==" \
--header "Accept: application/csv" \
--header "Content-Type: application/vnd.flux" \
--data 'from(bucket: "UEdata1") 
          |> range(start: -1h) 
          |> filter(fn: (r) => r._measurement == "UEThroughput") 
          |> limit(n: 10)'