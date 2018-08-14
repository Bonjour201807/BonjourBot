"""
@Author: yangdu
@Time: 2018/8/7 下午8:15
@Software: PyCharm
"""

import requests
import json

url = 'http://139.199.192.34:8080/v1/api/chatmessage/'
body = req = {'uid': '12345',
              'user_flag': 0,
              'message':
                  {'query': '天气？'}
              }
headers = {'content-type': "application/json"}

response = requests.post(url, data=json.dumps(body))

# 返回信息
print(response.text)
