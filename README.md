# List
Request:
```
GET /
```

Response
```
200 Ok

{
  "status": "ok",
  "volumes": [
    "test-blah3"
  ]
}
```

# Create
Request:
```
POST /volume/<namespace>/<name>

{
  "size": 1,
  "units": "GiB"
}
```

Response:
```
201 Created

{
  "status": "ok"
}
```

# Delete
Request:
```
DELETE /volume/<namespace>/<name>
```

Response:
```
200 Ok

{
  "status": "ok"
}
```
