import random

from bonjour.dm.policy.policy import Policy


class RunTask:
    def __init__(self):
        self.policy_handle = Policy()

    def run(self, request):
        policy_result = self.policy_handle.ploicy(request)
        if not policy_result:
            print('再见')
            return

        if policy_result['intent'] == 'weather':
            return self.exec_weather(policy_result)

    def exec_weather(self, policy_result: dict):
        if policy_result['tag'] == 0:
            return policy_result['question']
        elif policy_result['tag'] == 1:
            slots = policy_result['answer']['slot']
            wher = random.choice(['晴', '下雨', '刮风'])
            answer = '{}在{}的天气为{}'.format(slots['LOC'], slots['time'], wher)
            return answer
