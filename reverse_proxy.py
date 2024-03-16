from flask import Flask, request, redirect, Response, render_template, abort
import requests
from urllib.parse import urlparse
app = Flask(__name__)

# SITE_NAME = 'http://localhost:8000'
SITE_NAME_DICT = {
                   "manga.private": "http://localhost:5000",  # you can also use sock as "http://unix:/home/subrata32/stream-video-browser/hsecure1.sock"
                   "example2.com": "http://localhost:8000",  # you can also use sock as "http://unix:/home/subrata32/stream-video-browser/hsecure2.sock"
                   "example3.com": "http://localhost:9000",  # you can also use sock as "http://unix:/home/subrata32/stream-video-browser/hsecure3.sock"
                   "192.168.1.101": "http://localhost:10000"  # you can also use sock as "http://unix:/home/subrata32/stream-video-browser/hsecure4.sock"
}


def get_hostname_str(k=""):
    return str(urlparse(request.base_url).hostname)


@app.errorhandler(502)
def bad_gateway(e):
    return render_template('502.html'), 502


@app.route('/check')
def index():
    print(str(urlparse(request.base_url).hostname))
    return 'Flask is running!'


@app.route('/<path:path>',methods=['GET','POST','DELETE'])
def proxy(path):
    global SITE_NAME_DICT
    SITE_NAMEY = get_hostname_str(k=request.base_url)
    if SITE_NAMEY in SITE_NAME_DICT:
        SITE_NAME = SITE_NAME_DICT[SITE_NAMEY]
        if request.method == 'GET':
            print(f'{SITE_NAME}/{path}')
            resp = requests.get(f'{SITE_NAME}/{path}')
            excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
            headers = [(name, value) for (name, value) in  resp.raw.headers.items() if name.lower() not in excluded_headers]
            response = Response(resp.content, resp.status_code, headers)
            return response
        elif request.method == 'POST':
            print(f'{SITE_NAME}/{path}')
            resp = requests.post(f'{SITE_NAME}/{path}', json=request.get_json())
            excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
            headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
            response = Response(resp.content, resp.status_code, headers)
            return response
        elif request.method == 'DELETE':
            resp = requests.delete(f'{SITE_NAME}/{path}').content
            response = Response(resp.content, resp.status_code, headers)
            return response
    else:
        abort(502)


if __name__ == '__main__':
    app.run("0.0.0.0", debug=False, port=80)
