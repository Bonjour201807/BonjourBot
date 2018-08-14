"""
@Author: yangdu
@Time: 2018/8/4 下午5:27
@Software: PyCharm
"""
from collections import defaultdict
from bonjour.dm.policy.policy import Policy
from bonjour.utils import logger


class RunTask:
    def __init__(self):
        self.policy_handle = Policy()

    def run(self, request):
        policy_result = self.policy_handle.policy(request)
        logger.debug('plolicy_result,{}'.format(policy_result))
        if not policy_result:
            return None

        elif policy_result['intent'] == 'weather':
            return self.exec_weather(policy_result)

        else:
            return None

    def exec_weather(self, policy_result: dict):
        reply = {'flag': None,
                 'message': defaultdict(dict)}
        if policy_result['tag'] == 0:
            reply['flag'] = 0
            reply['message']['text'] = policy_result['question']
            return reply
        elif policy_result['tag'] == 1:
            slots = policy_result['answer']['slot']
            reply['flag'] = 5
            reply['message']['local'] = slots['LOC'][0]
            reply['message']['start_time'] = slots['start_time']
            reply['message']['delta_time'] = slots['delta_time']
            return reply
