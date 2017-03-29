# Launch app
## Docker
```
docker run -d \
  -v /var/run/tgtd/socket.0:/var/run/tgtd/socket.0 \
  -v /etc/tgt/conf.d:/etc/tgt/conf.d \
  --privileged \
  --network=host \
  volcreate:latest -g iiot --host=0.0.0.0
```

## Available options 
```
Usage: volcreate.py [options]

Options:
  -h, --help            show this help message and exit
  -g VG_NAME, --group=VG_NAME
                        VG name to use
  --host=HOST           IP address to listen
  -p PORT, --port=PORT  Port to listen
  -i ISCSI_STORAGE, --iscsi-storage=ISCSI_STORAGE
                        SAN network IQN part of iSCSI storage name
  --tgt-confdir=TGT_CONFDIR
                        tgt daemon config file directory
```

# API
## List volumes
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

## Create volume
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

## Delete volume
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

## Create iSCSI target
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

## Delete iSCSI target
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
