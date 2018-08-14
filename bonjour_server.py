"""
@Author: yangdu
@Time: 2018/8/4 下午5:50
@Software: PyCharm
"""
import json
from bonjour.agent.agent import Agent
from bonjour.utils import logger
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
logger.setLevel('DEBUG')
agenter = Agent()
CORS(app, supports_credentials=True)

@app.route('/v1/api/chatmessage/', methods=['GET'])
def chat_bot():
    # if request.method == 'POST':
    #     req_dct = json.loads(request.data)
    # else:
    logger.info(request.args)
    req_dct = dict()
    req_dct['uid'] = request.args.get('uid')
    req_dct['user_flag'] = json.loads(request.args.get('user_flag'))
    req_dct['message'] = json.loads(request.args.get('message'))
    logger.debug(req_dct)
    return json.dumps(agenter.response(req_dct))


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0',port=8080)
