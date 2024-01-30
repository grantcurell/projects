
# Stuff I tried that didn't work

## GDAL Attempt (Does not work)

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

## Metricbeat Install Attempt (Does not work)

**If you want to make it easy don't set up security, but !**

Run with `podman run -v /opt/elasticsearch:/usr/share/elasticsearch/data --privileged -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -e xpack.security.enabled=true -e xpack.monitoring.collection.enabled=true -e ES_JAVA_OPTS="-Xms16g [53/53]" docker.elastic.co/elasticsearch/elasticsearch:7.7.0`
to run Elasticsearch with security enabled.

I ran `chmod -R 774 /opt/elasticsearch` to change the permissions to allow `podman`
to run unpriveleged.

If you need to, you can double check the heap size with:

`curl -sS -XGET "localhost:9200/_cat/nodes?h=heap*&v"`

If you want to use Metricbeat you'll also have to enable security and configure
users. Do the following:

1. Install Metricbeat from [here](https://www.elastic.co/guide/en/beats/metricbeat/current/metricbeat-installation.html)
2. Before starting Metricbeat, go in to the config file at `/etc/metricbeat/metricbeat.yml` and make sure you have the dashboard upload enabled.
3. Next, you'll need to exec into your Elasticsearch container and setup passwords.
      1.Run `podman exec -it <CONTAINER_ID> /bin/bash` to get a command line on the container.
      2.Run `/usr/share/elasticsearch/bin/elasticsearch-setup-passwords interactive` to setup passwords.
4. Run `cd /etc/metricbeat` then run `metricbeat modules enable elasticsearch-xpack`
5. Then edit `/etc/metricbeat/metricbeat.yml` Make sure the output hosts are correct and then change username and password to what you set earlier.
      1.Also make sure that the Kibana host is set correctly.
6. You'll also need to set the Kibana user in `/etc/kibana/kibana.yml`

## Helpful Links

Examples of usage [https://gist.github.com/nickpeihl/1a8f9cbecc78e9e04a73a953b30da84d](https://gist.github.com/nickpeihl/1a8f9cbecc78e9e04a73a953b30da84d)

[Ingest geospatial data into Elasticsearch with GDAL](https://www.elastic.co/blog/how-to-ingest-geospatial-data-into-elasticsearch-with-gdal)

[Elasticsearch Driver for GDAL Page](https://gdal.org/drivers/vector/elasticsearch.html)