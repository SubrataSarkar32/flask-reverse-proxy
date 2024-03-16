from flask import Flask, request, redirect, Response, render_template, abort
import requests
import os
from urllib.parse import urlparse


app = Flask(__name__)
path_to_file = "URL_DICT.txt"
SITE_NAME_DICT = {}


def process_url_dict(str_text=""):
    sitey = {}
    lines = str_text.split("\n")
    lines = [line for line in lines if (line != "" or line.startswith('#'))]
    for line in lines:
        two_part = line.split("->")
        key = two_part[0].replace('"', '').replace("'", "")
        value = two_part[1].replace('"', '').replace("'", "")
        sitey[key] = value
    return sitey


if os.path.exists(path_to_file):
    file1 = open(path_to_file, "r")
    file_out = file1.read()
    file1.close()
    SITE_NAME_DICT = process_url_dict(str_text=file_out)

if SITE_NAME_DICT == {}:
    SITE_NAME_DICT = {
                    "example.private": "http://localhost:5000",  # you can also use sock as "http://unix:/home/subrata32/stream-video-browser/hsecure1.sock"
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


@app.route('/', methods=['GET', 'POST', 'DELETE'])
def proxy1():
    global SITE_NAME_DICT
    print(SITE_NAME_DICT)
    SITE_NAMEY = get_hostname_str(k=request.base_url)
    try:
        if SITE_NAMEY in SITE_NAME_DICT:
            SITE_NAME = SITE_NAME_DICT[SITE_NAMEY]
            if request.method == 'GET':
                print(f'{SITE_NAME}/')
                resp = requests.get(f'{SITE_NAME}/')
                excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
                headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
                response = Response(resp.content, resp.status_code, headers)
                return response
            elif request.method == 'POST':
                print(f'{SITE_NAME}/')
                resp = requests.post(f'{SITE_NAME}/', json=request.get_json())
                excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
                headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
                response = Response(resp.content, resp.status_code, headers)
                return response
            elif request.method == 'DELETE':
                resp = requests.delete(f'{SITE_NAME}/').content
                response = Response(resp.content, resp.status_code, headers)
                return response
        else:
            abort(502)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        abort(502)


@app.route('/<path:path>', methods=['GET', 'POST', 'DELETE'])
def proxy(path):
    global SITE_NAME_DICT
    SITE_NAMEY = get_hostname_str(k=request.base_url)
    try:
        if SITE_NAMEY in SITE_NAME_DICT:
            SITE_NAME = SITE_NAME_DICT[SITE_NAMEY]
            if request.method == 'GET':
                print(f'{SITE_NAME}/{path}')
                resp = requests.get(f'{SITE_NAME}/{path}')
                excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
                headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
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
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        abort(502)


if __name__ == '__main__':
    app.run("0.0.0.0", debug=False, port=80)
