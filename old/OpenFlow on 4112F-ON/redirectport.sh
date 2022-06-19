#!/bin/bash

curl -X PUT -d '{"operation": "add", "tcp_port" : 80, "out_port" : 1}' http://127.0.0.1:8080/gelante/redirectport/150013889525632
