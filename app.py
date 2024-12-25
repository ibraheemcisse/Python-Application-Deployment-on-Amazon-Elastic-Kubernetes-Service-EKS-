from flask import Flask, Response
from prometheus_client import Counter, generate_latest

app = Flask(__name__)


REQUESTS = Counter('http_requests_total', 'Total number of HTTP requests')

@app.route('/')
def hello():
    REQUESTS.inc()  
    return 'Hello, World!'

@app.route('/metrics')
def metrics():
    return Response(generate_latest(REQUESTS), mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
