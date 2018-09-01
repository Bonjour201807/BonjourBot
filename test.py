"""
@Author: yangdu
@Time: 2018/8/7 下午8:15
@Software: PyCharm
"""

import requests
import json
from bonjour.agent.agent import Agent
#
# url = 'http://132.232.67.192:8088/v1/api/chatmessage/'
# # url = 'http://localhost:8085/v1/api/chatmessage/'
#
# body = {'uid': 'azx1', 'user_flag': 0, 'message': json.dumps({'query': '明天'})}
# # body = {'uid': 'azx1', 'user_flag': 1, 'message': json.dumps({'days': 1, 'departure': '深圳市'})}
# # body = {'uid': 'azx1', 'user_flag': 2, 'message': json.dumps({'input_tags': ['古建筑','科技'], 'select_tags': ['大学']})}
#
#
# res = requests.get(url, params=body)
# print(res)
# # 返回信息
# print(res.json())

agenter = Agent()
print(agenter.response({'uid': 'azx111', 'user_flag': 0, 'message': {'query': '红烧肉怎么做'}}))
print(agenter.response({'uid': 'azx111', 'user_flag': 0, 'message': {'query': '天气'}}))
print(agenter.response({'uid': 'azx111', 'user_flag': 0, 'message': {'query': '深圳'}}))
print(agenter.response({'uid': 'azx111', 'user_flag': 0, 'message': {'query': 'hahha'}}))
print(agenter.response({'uid': 'azx111', 'user_flag': 0, 'message': {'query': 'hahha'}}))
print(agenter.response({'uid': 'azx111', 'user_flag': 0, 'message': {'query': 'hahha'}}))
print(agenter.response({'uid': 'azx111', 'user_flag': 0, 'message': {'query': '明天'}}))
print(agenter.response({'uid': 'azx111', 'user_flag': 0, 'message': {'query': '红烧肉怎么做'}}))

# print(agenter.response({'uid': 'azx11', 'user_flag': 1, 'message': {'days': 1, 'departure': '深圳市'}}))
# print(agenter.response({'uid': 'azx11', 'user_flag': 2, 'message': {'input_tags': ['古建筑','科技'], 'select_tags': ['大学']}}))
# print(agenter.response({'uid': 'azx11', 'user_flag': 2, 'scroll_id': 10}))
