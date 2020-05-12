# Use Elasticsearch to Display a Set of Map Data

## Installation

1. [Install CRI-O](https://github.com/cri-o/cri-o/blob/master/tutorials/setup.md#rhel-8)
2. Install Kibana.


## Running Elasticsearch with Podman

### Set VM Max Map

In `/etc/sysctl.conf` add `vm.max_map_count=262144`

### Turn off swap

`sudo swapoff -a`

### Running Elasticsearch

`podman run -v /opt/elasticsearch:/usr/share/elasticsearch/data --privileged  -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -e ES_JAVA_OPTS="-Xms28g -Xmx28g" docker.elastic.co/elasticsearch/elasticsearch:7.6.2`

I also gave all privs to /opt/elasticsearch because I didn't want to go to the trouble of figuring out what the proper UID is. Sue me.

If you need to, you can double check the heap size with:

`curl -sS -XGET "localhost:9200/_cat/nodes?h=heap*&v"`

## Importing the Data into Elasticsearch

1. I worte the code in [main.py](./code/main.py) to take a CSV I got from [ACLED](https://acleddata.com/) into geoJSON formatted data. The program [format.py](./code/format.py) just formatted the 30 fields into the Python program for ease of use.
   1. Modify the code as necessary and then run to get geoJSON formatted data.


### Upload the Mapping

First you have to create the index with `curl -X PUT "localhost:9200/conflict-data?pretty"`

Then you can upload the mapping with: `curl -X PUT localhost:9200/conflict-data/_mapping?pretty -H "Content-Type: application/json" -d @mapping.json`

## Helpful Links

Examples of usage [https://gist.github.com/nickpeihl/1a8f9cbecc78e9e04a73a953b30da84d](https://gist.github.com/nickpeihl/1a8f9cbecc78e9e04a73a953b30da84d)

[Ingest geospatial data into Elasticsearch with GDAL](https://www.elastic.co/blog/how-to-ingest-geospatial-data-into-elasticsearch-with-gdal)

[Elasticsearch Driver for GDAL Page](https://gdal.org/drivers/vector/elasticsearch.html)

## Scrapped Idea

I originally tried to push the data with GDAL, but wasn't sure how to get the syntax to work.

Kibana only allows you to upload 50 MB files so ingest must be done manually. I'm using GDAL. [Install here](https://trac.osgeo.org/gdal/wiki/DownloadingGdalBinaries)

   1. `wget https://github.com/OSGeo/gdal/releases/download/v3.1.0/gdal-3.1.0.tar.gz`
   2. `tar xf gdal*`
   3. On RHEL8 run `dnf install -y gcc-toolset-9 && scl enable gcc-toolset-9 bash`.
      1. This will install gcc v.9 and will open a new bash shell using v9 with appropriate environment variables.
   4. On Ubuntu do the following:
         ```
         sudo add-apt-repository ppa:ubuntu-toolchain-r/test
         sudo apt update
         sudo apt install gcc-9 pkg-config
         ```
   5. You will need project 6 from `https://download.osgeo.org/proj/proj-6.0.0.zip`
      1. Run `dnf install -y sqlite-devel && ./configure && make && make install`
   6. You will need to install jasper and libcurl-devel with `dnf install -y jasper-devel libcurl-devel`
   7. Now run `./configure --with-proj=/usr/local && make -j <as many as possible> && make install`
      1. The make takes an eternity if you don't give it more threads.

For utility you may want to install EPEL with `sudo dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm`

Creating a mapping with GDAL: `ogr2ogr -overwrite -lco INDEX_NAME=gdal-data -lco NOT_ANALYZED_FIELDS={ALL} -lco WRITE_MAPPING=./mapping.json ES:http://localhost:9200 GeoObs.json`

Uploading with GDAL: `ogr2ogr -lco INDEX_NAME=gdal-data -lco OVERWRITE_INDEX=YES -lco MAPPING=./mapping.json ES:http://localhost:9200 GeoObs.json`

2. You can run `ogrinfo ES:http://localhost:9200` to check the indicies in your Elasticsearch instance and make sure that everything is connected and ready to go.