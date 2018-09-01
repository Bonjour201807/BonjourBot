"""
@Author: yangdu
@Time: 2018/9/1 上午12:18
@Software: PyCharm
"""

import requests
import json


class TulinBot:
    url = 'http://openapi.tuling123.com/openapi/api/v2'
    api_key = 'bb4f1e0af9a549539744415112588cbe'
    req = {
        "reqType": 0,
        "perception": {
            "inputText": {
                "text": ''
            }
        },
        "userInfo": {
            "apiKey": api_key,
            "userId": ""
        }
    }

    @classmethod
    def get_answer(cls, uid=None, text=None):
        if not uid or not text:
            return None

        cls.req['perception']['inputText']['text'] = text
        cls.req['userInfo']['userId'] = uid

        res = requests.post(cls.url, data=json.dumps(cls.req)).json()

        if res['intent']['code'] in [10003, 10004, 10009, 10006, 10010, 10011, 10041, 10022,
                                     10030, 10031, 10032, 10033, 10034, 10019]:
            text = res['results'][0]['values']['text']
            ret = {'flag': 0,
                   'message': {'text': text}}
            return ret

        if res['intent']['code'] in [10014, 10005]:
            text = res['results'][1]['values']['text']+'\n'+res['results'][0]['values']['url']
            ret = {'flag': 0,
                   'message': {'text': text}}
            return ret

        if res['intent']['code'] in [10015]:
            recipe = ''
            for item in res['results'][1]['values']['news'][:3]:
                recipe += 'name: '+item['name']+'\n'+\
                    'info: '+item['info']+'\n'+\
                    'detailurl: '+item['detailurl']
                recipe += '\n\n'
            text = res['results'][0]['values']['text'] + '\n' + recipe
            ret = {'flag': 0,
                   'message': {'text': text}}
            return ret


if __name__ == '__main__':
    print(TulinBot.get_answer(uid='12345', text='附近的酒店'))
    print(TulinBot.get_answer(uid='12345', text='帮我找个杯子的图片'))