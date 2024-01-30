import requests
import logging

from_kibana = 'https://192.168.1.235:5601'
to_kibana = 'https://192.168.1.100:5601'

r = requests.get(from_kibana + '/api/saved_objects/_find?type=map')

js = r.json()

mapconfig = js['saved_objects'][0]['attributes']

mapout = {'attributes': mapconfig}

p = requests.post(to_kibana + '/api/saved_objects/map/vehicles', json=mapout, headers={'kbn-xsrf': 'true'})

logging.info(p)
logging.info(p.json())
logging.info('check that map was uploaded')

r = requests.get(to_kibana + '/api/saved_objects/_find?type=map')
logging.info(r.text)
