# Elasticsearch Display Map Data

## Environment

CentOS7

I tried this first with RHEL8 and the backend docker networking didn't work

## Installation

Install docker with the following:

      yum install -y https://download.docker.com/linux/centos/7/x86_64/stable/Packages/containerd.io-1.2.6-3.3.el7.x86_64.rpm epel-release
      yum config-manager --add-repo=https://download.docker.com/linux/centos/docker-ce.repo
      yum install -y docker python-pip python36
      curl -L "https://github.com/docker/compose/releases/download/1.25.5/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
      chmod +x /usr/local/bin/docker-compose
      systemctl enable docker
      systemctl start docker
      pip3.6 install geojson elasticsearch

## Running Elasticsearch with Docker

### Set VM Max Map

In `/etc/sysctl.conf` add `vm.max_map_count=262144`

### Turn off swap

`sudo swapoff -a`

### Setup Data Directories

If you are bind-mounting a local directory or file, it must be readable by the elasticsearch user. In addition, this user must have write access to the data and log dirs. A good strategy is to grant group access to gid 0 for the local directory.

For example, to prepare a local directory for storing data through a bind-mount:

      mkdir /opt/
      mkdir /opt/data01
      mkdir /opt/data02
      mkdir /opt/data03
      mkdir /opt/data04

      chmod g+rwx /opt/data*
      chgrp 0 /opt/data*
      chmod 777 -R /opt/data*

^ I got lazy. Not sure what the permissions issue is, but I couldn't get the
volumes to mount so I gave up and set it to 777. My best guess is that the
real problem is it isn't running as user 0 because that's root. It's probably
something else.

### Running Elasticsearch

1. Copy over the docker compose file
2. Now, you must run docker-compose *in the folder in which you have the directories*. Otherwies you get a permissions error. cd `/var/elasticsearch-data/` then run `docker-compose up`

## Importing the Data into Elasticsearch

1. I wrote the code in [csv2geojson.py](./code/csv2geojson.py) to take a CSV I got from [ACLED](https://acleddata.com/) into geoJSON formatted data. The program [format.py](./code/format.py) just formatted the 30 fields into the Python program for ease of use.
      1.Modify the code as necessary and then run to get geoJSON formatted data.
2. Next you'll need to upload the mapping file.
      1.First you have to create the index with

            curl -X PUT "localhost:9200/conflict-data?pretty" -H 'Content-Type: application/json' -d'
            {
               "settings" : {
                  "index" : {
                        "number_of_shards" : 4, 
                        "number_of_replicas" : 3
                  }
               }
            }
            '

      2.Then you can upload the mapping with: `curl -X PUT localhost:9200/conflict-data/_mapping?pretty -H "Content-Type: application/json" -d @mapping.json`
3. Now you can import the data with [index_data.py](code/index_data.py). **NOTE** Make sure you use `python3.6`
      1.You may have to modify the code a bit to get it to ingest properly.

### Configuring Metricbeat in a container

First double check the name of your elastic network with `docker network ls`
It's probably opt_elastic. Docker compose prefixes everything with the directory
from which you're running unless you specify the `-p` option.

1. Pull the container and then run the setup

         cd /opt
         docker pull docker.elastic.co/beats/metricbeat:7.7.0
         docker run --network opt_elastic docker.elastic.co/beats/metricbeat:7.7.0 setup -E setup.kibana.host=kib01:5601 -E output.elasticsearch.hosts=["es01:9200"]

2. Copy the metricbeat.yml to /opt


## Importing Map from Somewhere Else

Online it will tell you that you need code to import and export objects. This is
no longer the case. When I tested in 7.7.0 you could export saved objects from
the saved objects menu in Kibana and then import them on the other side. I included
the CPU load gauges, my custom queries, and the maps. Import the three ndjson
files included in the repo.

## Helpful Commands

### Check Heap Size

`curl -sS -XGET "localhost:9200/_cat/nodes?h=heap*&v"`

#### Remove Exited Containers

`sudo docker rm $(docker ps -a -f status=exited -q)`

## Running A Single Elasticsearch Instance

`docker run -v /opt/elasticsearch:/usr/share/elasticsearch/data --privileged  -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -e ES_JAVA_OPTS="-Xms28g -Xmx28g" docker.elastic.co/elasticsearch/elasticsearch:7.7.0`


