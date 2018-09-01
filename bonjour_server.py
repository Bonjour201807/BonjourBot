"""
@Author: yangdu
@Time: 2018/8/4 下午5:50
@Software: PyCharm
"""
import json
from bonjour.agent.agent import Agent
# from bonjour.agent.es_api import tags_scroll, attractions_scroll
from bonjour.agent.search import tags_scroll, spots_scroll
from bonjour.utils import logger
from flask import Flask, request
from flask_cors import CORS


app = Flask(__name__)
logger.setLevel('INFO')
agenter = Agent()
CORS(app, supports_credentials=True)


@app.route('/v1/api/chatmessage/', methods=['GET'])
def chat_bot():
    logger.info(request.args)
    req_dct = dict()
    req_dct['uid'] = request.args.get('uid')
    size = request.args.get('size')
    if isinstance(size, str):
        size = int(size)
    req_dct['size'] = size
    print('request.args', request.args)
    req_dct['user_flag'] = json.loads(request.args.get('user_flag'))
    req_dct['message'] = json.loads(request.args.get('message'))
    return json.dumps(agenter.response(req_dct))


@app.route('/v1/api/tags/', methods=['GET'])
def tags_scroll_():
    req_dct = dict()
    req_dct['uid'] = request.args.get('uid')
    size = request.args.get('size')
    if isinstance(size, str):
        size = int(size)
    req_dct['size'] = size
    req_dct['from_page'] = int(request.args.get('from_page'))
    req_dct['data'] = json.loads(request.args.get('data'))
    res = tags_scroll(req_dct)
    return json.dumps(res)


@app.route('/v1/api/spots/', methods=['GET'])
def spots_scroll_():
    req_dct = dict()
    req_dct['uid'] = request.args.get('uid')
    req_dct['size'] = int(request.args.get('size'))
    req_dct['from_page'] = int(request.args.get('from_page'))
    req_dct['data'] = json.loads(request.args.get('data'))
    res = spots_scroll(req_dct)
    print('spots_scroll',res)
    return json.dumps(res)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8088)
