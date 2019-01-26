#!/usr/bin/env python3

import http.server
import socketserver
from lxml import html
from lxml import etree
import json
import requests
import time
from flask import Flask, request, jsonify

app = Flask(__name__)
users_seen = {}

@app.route('/', methods=["GET","POST"])
def hello():
    user_agent = request.headers.get('User-Agent')
    parse = request.json
    # parse = json.loads(json_data)
    page = requests.get(parse['url'])
    pageDom = html.fromstring(page.text)

    result = {}

    # print(page.text)

    def getText(elem):

        if type(elem) is html.HtmlElement:
            return elem.text
        if type(elem) is etree._ElementUnicodeResult:
            return elem
        else:
            print(type(elem))
            return elem

    for x in parse['map']:
        elem = pageDom.xpath(parse['map'][x])
        for i in elem:
            if x in result:
                result[x].append(getText(i))
            else:
                result[x] = []
                result[x].append(getText(i))


    return jsonify(success=True, msg="It's On", result=result)

@app.route('/checkin/<user>', methods=['POST'])
def check_in(user):
    users_seen[user] = time.strftime('%Y-%m-%d')
    return jsonify(success=True, user=user)

@app.route('/last-seen/<user>')
def last_seen(user):
    if user in users_seen:
        return jsonify(user=user, date=users_seen[user])
    else:
        return jsonify(error='Who dis?', user=user), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


#
# json_data = '{ "url" : "http://www.google.com.br", "map" : { "title": "//title", "body": "//body",  "meta" : "//meta/@content"} }'
#
# parse = json.loads(json_data)
# page = requests.get(parse['url'])
# pageDom = html.fromstring(page.text)
#
# result = {}
#
# #print(page.text)
#
#
# def getText(elem):
#
#     if type(elem) is html.HtmlElement:
#         return elem.text
#     if type(elem) is etree._ElementUnicodeResult:
#         return elem
#     else:
#         print(type(elem))
#         return elem
#
# for x in parse['map']:
#     elem = pageDom.xpath(parse['map'][x])
#     for i in elem:
#         if x in result:
#             result[x].append(getText(i))
#         else:
#             result[x] = []
#             result[x].append(getText(i))
#
# print(result)


