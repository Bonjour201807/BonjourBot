"""
@Author: yangdu
@Time: 2018/8/4 下午5:27
@Software: PyCharm
"""
from collections import defaultdict
from bonjour.dm.policy import Policy
from bonjour.nlu import NLU


class RunTask:
    def __init__(self):
        self.policy_handle = Policy()
        self.nlu_handle = NLU()

    def process(self, request: dict):
        '''

        :param request: 必须包含字段: type
        如果type==0, 格式为必须为{'type':0,uid:'1234'，query:'你好'}，
        如果type==1，格式为必须为{'type':1,'intent':'',slot:{'LOC':''},uid:'1234'},其中uid的值不能为空，intent和slot
        可以
        :return:
        '''

        if request['type'] == 0:
            intent_slot_dct = self.nlu_handle.parse(request['query'])
            intent_slot_dct['uid'] = request['uid']
            policy_result = self.policy_handle.process(intent_slot_dct)
        else:
            policy_result = self.policy_handle.process(request)

        if not policy_result:
            return None

        intent_name = policy_result['intent']
        if intent_name:
            return self.run(intent_name, policy_result)
        else:
            return None

    def run(self, intent_name: str, policy_result: dict):
        func_name = 'exec_'+intent_name
        func = 'self.{}({})'.format(func_name, policy_result)
        return eval(func)

    @staticmethod
    def exec_weather(policy_result: dict):
        assert 'weather' == policy_result['intent']
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
        else:
            return None

    @staticmethod
    def exec_play(policy_result: dict):
        assert 'play' == policy_result['intent']
        pass


if __name__ == '__main__':
    tasker = RunTask()
    # req = {'type':1,'intent':'weather','slot':{'LOC':'深圳'},'uid':'0003'}
    req = {'type':0,'query':'明天','uid':'0003'}
    print(tasker.process(req))