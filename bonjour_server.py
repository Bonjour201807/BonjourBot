"""
@Author: yangdu
@Time: 2018/8/4 下午5:50
@Software: PyCharm
"""
import json
from bonjour.agent.agent import Agent
from bonjour.agent.es_api import tags_scroll, attractions_scroll
from bonjour.utils import logger
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
logger.setLevel('INFO')
agenter = Agent()
CORS(app, supports_credentials=True)


@app.route('/v1/api/chatmessage/', methods=['GET'])
def chat_bot():
    # if request.method == 'POST':
    #     req_dct = json.loads(request.data)
    # else:
    logger.info(request.args)
    print(request.args)
    req_dct = dict()
    req_dct['uid'] = request.args.get('uid')
    req_dct['user_flag'] = json.loads(request.args.get('user_flag'))
    req_dct['message'] = json.loads(request.args.get('message'))
    logger.debug(req_dct)
    #print('json.dumps(agenter.response(req_dct))',json.dumps(agenter.response(req_dct)))
    return json.dumps(agenter.response(req_dct))


@app.route('/v1/api/tags/scroll/', methods=['GET'])
def tags_scroll():
    uid = request.args.get('uid')
    scroll_id = request.args.get('scroll_id')
    res = tags_scroll(uid, scroll_id)
    return json.dumps(res)


@app.route('/v1/api/attractions/scroll/', methods=['GET'])
def attractions_scroll():
    uid = request.args.get('uid')
    scroll_id = request.args.get('scroll_id')
    res = attractions_scroll(uid=uid, scroll_id=scroll_id)
    return json.dumps(res)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8088)
