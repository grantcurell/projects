import geojson
from datetime import datetime
from elasticsearch import Elasticsearch, helpers


def geojson_to_es(gj):

    for feature in gj['features']:

        date = datetime.strptime("-".join(feature["properties"]["event_date"].split('-')[0:2]) + "-" + feature["properties"]["year"], "%d-%B-%Y")
        feature["properties"]["timestamp"] = int(date.timestamp())
        feature["properties"]["event_date"] = date.strftime('%Y-%m-%d')
        yield feature


with open("test_point.json") as f:
    gj = geojson.load(f)

    es = Elasticsearch(hosts=[{'host': 'localhost', 'port': 9200}])

    k = ({
        "_index": "conflict-data",
        "_type": "_doc",
        "_source": feature,
    } for feature in geojson_to_es(gj))

    helpers.bulk(es, k)
