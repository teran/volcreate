# List volumes
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

# Create volume
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

# Delete volume
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

# Create iSCSI target
Request:
```
POST /tgt/<namespace>/<name>

{
  "initiator": "10.0.0.0/24"
}
```

Response:
```
201 Created

{
  "status": "ok"
}
```

# Delete iSCSI target
Request:
```
DELETE /tgt/<namespace>/<name>
```

Response:
```
200 Ok

{
  "status": "ok"
}
```
