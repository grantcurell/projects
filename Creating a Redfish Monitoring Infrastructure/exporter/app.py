import os
from flask import Flask, Response

app = Flask(__name__)

METRICS_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), '../poller/metrics.prom'))

@app.route("/metrics")
def metrics():
    if os.path.exists(METRICS_FILE):
        with open(METRICS_FILE, "r") as f:
            data = f.read()
    else:
        data = "# no metrics found\n"
    return Response(data, mimetype="text/plain")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
