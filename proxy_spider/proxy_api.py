from flask import Flask, g
from proxy_spider.proxy_db import MysqlClient

__all__ = ['app']

app = Flask(__name__)

def get_conn():
    if not hasattr(g, 'mysql'):
        g.mysql = MysqlClient
    return g.mysql

@app.route('/')
def index():
    return '<h2>welcome to proxy system</h2>'

@app.route('/random')
def get_proxy():
    conn = get_conn()
    # TypeError: randomIP() missing 1 required positional argument: 'self'
    # 127.0.0.1 - - [29/Oct/2020 08:57:31] "GET /random HTTP/1.1" 500 -
    return conn.randomIP()

@app.route('/count')
def get_count():
    conn = get_conn()
    # TypeError: count() missing 1 required positional argument: 'self'
    # 127.0.0.1 - - [29/Oct/2020 08:57:54] "GET /count HTTP/1.1" 500 -
    return str(conn.count())

if __name__ == "__main__":
    app.run()