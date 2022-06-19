#!/bin/bash

curl -X PUT -d '{"operation": "add", "openflow_port": 1}' http://192.168.1.6:8080/gelante/outports/150013889525632
curl -X PUT -d '{"operation": "add", "openflow_port": 5}' http://192.168.1.6:8080/gelante/outports/150013889525632
curl -X PUT -d '{"operation": "add", "openflow_port": 9}' http://192.168.1.6:8080/gelante/inports/150013889525632
echo ""
