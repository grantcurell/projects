import re
from flask import Flask, request, Response, render_template
from werkzeug.routing import BaseConverter

app = Flask(__name__)


# Built from https://stackoverflow.com/a/5872904/4427375
class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app.url_map.converters['regex'] = RegexConverter

# See https://stackoverflow.com/a/7629690/4427375 for logic
mac_address_regex = re.compile(r"[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\1[0-9a-f]{2}){4}$")


@app.route('/<regex("[a-z0-9]{12}"):mac_address>.json/')
def config(mac_address):
    print("Processing MAC address " + mac_address)
    return render_template('configs/config_db.json', gwaddr='192.168.1.1', mgmt_address="192.168.1.94/24")


@app.route('/initial.json')
def initial():
    print(request.headers)
    print(request.headers['User-Agent'])

    # TODO - some logic about checking the MAC address list.

    if 'Base-Mac-Address' in request.headers:
        if mac_address_regex.match(request.headers['Base-Mac-Address'].lower()):
            config_name = request.headers['Base-Mac-Address'].lower().replace(':', '')
            return render_template('initial.json', ip_address='192.168.1.6', config_name=config_name)
        return Response("Error: Received a malformed MAC address " + request.headers['Base-Mac-Address'], status=400)
    else:
        return Response("Error: Base-Mac-Address missing from HTTP headers.", status=400)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
