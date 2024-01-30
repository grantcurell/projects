# Importing Elasticsearch Data

**WARNING** These instructions are rough.

1. Move your Elasticsearch snapshot folder to a known folder. For our example, I used `/opt/snapshots`.
2. Next you will need to tell Elasticsearch about this path by adding the `path.repo` directive in the configuration file. Run:

        vim /etc/elasticsearch/elasticsearch.yml

        # Add
        `path.repo: ["/opt/snapshots"]`

3. Now you need to import the data itself into Elasticsearch. Import with:

        curl -X PUT "localhost:9200/_snapshot/esdata?pretty" -H 'Content-Type: application/json' -d'
        {
            "type": "fs",
            "settings": {
                "location": "/opt/snapshots",
                "compress": true
            }
        }
        '

Note: It took about 5 minutes for the snapshot to load

4. Next you will need to restore the snapshot by doing the following: Go to management, saved objects, import, select file on your local computer
5. Import dashboards into Elasticsearch `curl -O http://192.168.122.1:8000/kibana-export.json`

## Helpful Commands

View a list of the snapshots:

    curl localhost:9200/_cat/snapshots/esdata
    curl -X GET "localhost:9200/_snapshot/_status?pretty"

Restore the snapshot with:

    curl -X POST "localhost:9200/_snapshot/esdata/snapshot_1/_restore?pretty"

# Install Moloch

1. Run `yum install -y https://files.molo.ch/builds/centos-7/moloch-1.1.1-1.x86_64.rpm`
2. Configure Moloch with `/data/moloch/bin/Configure`
3. Run `/data/moloch/db/db.pl http://ESHOST:9200 init` to init the cluster
4. Add user `/data/moloch/bin/moloch_add_user.sh admin "Admin User" password --admin`
5. Import your data with `./bin/moloch-capture -c etc/config.ini -R <YOUR_DIRECTORY>`. You can import individual files with lowercase -r.

