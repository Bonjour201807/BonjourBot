"""
@Author: yangdu
@Time: 2018/8/4 下午5:27
@Software: PyCharm
"""
import json

from bonjour.agent.amap_api import Amap
from bonjour.agent.external_api import TulinBot
from bonjour.agent.run_task import RunTask
from bonjour.agent.search_api import Search
from bonjour.nlu.intent_detection.intent_detection import Intent
from bonjour.utils.utils import *
from bonjour.utils.db_helper import redis_handle

intenter = Intent()


class Agent:
    def __init__(self):
        self._task_runner = RunTask()

    def response(self, req: dict):
        """
        :param req: 包含字段uid:str,user_flag:int,message:dict
        :return:
        """
        if req['user_flag'] == 0 or req['user_flag'] == '0':
            req_dct = dict()
            uid = req['uid']
            query = req['message']['query']
            req_dct['uid'] = req['uid']
            req_dct['query'] = query
            req_dct['type'] = 0
            cly = self.dispatch(uid, query)
            print('{}--cly:{}'.format(query,cly))

            if cly == 1:
                ret = self._task_runner.process(req_dct)
                if ret:
                    redis_handle.lpush(uid + '.query_history', json.dumps({'query': query, 'who': 0}))
                    redis_handle.lpush(uid + '.query_history', json.dumps({'answer': ret, 'who': 1}))
                    return ret
                else:
                    ret = TulinBot.get_answer(uid=uid, text=query)
                    redis_handle.lpush(uid + '.query_history', json.dumps({'query': query, 'who': 0}))
                    redis_handle.lpush(uid + '.query_history', json.dumps({'answer': ret, 'who': 2}))
                    return ret
            elif cly == 2:
                ret = TulinBot.get_answer(uid=uid, text=query)
                redis_handle.lpush(uid + '.query_history', json.dumps({'query': query, 'who': 0}))
                redis_handle.lpush(uid + '.query_history', json.dumps({'answer': ret, 'who': 2}))
                return ret
            return TulinBot.get_answer(uid=uid, text=query)

        elif req['user_flag'] == 1 or req['user_flag'] == '1':
            distance = cvt_days(req['message']['days'])
            loc = Amap.geocode(req['message']['departure'])
            size = req['size']
            if distance and loc:
                # redis_handle.set(req['uid']+':info', {'distance': distance, 'loc': loc})
                res = Search.get_tags_by_loc_distance(loc=loc, distance=distance, size=size)
                ret = {'flag': 2,
                       'message': {'text': '您可能感兴趣的标签: ',
                                   'data': res['data']}}
                return ret
            else:
                return None

        elif req['user_flag'] == 2 or req['user_flag'] == '2':
            # print(redis_handle.get(req['uid']+':info'))
            # user_info = eval(redis_handle.get(req['uid']+':info'))
            distance = cvt_days(req['message']['days'])
            loc = Amap.geocode(req['message']['departure'])
            tags = req['message']['select_tags'] + [req['message']['input_tag']]
            size = req['size']
            if isinstance(size, str):
                size = int(size)

            res = Search.get_spots_by_loc_distance_tags(loc=loc, distance=distance, tags=tags, size=size)
            ret = {'flag': 3,
                   'message': {'data': res['data']}}
            return ret

        elif req['user_flag'] == 3 or req['user_flag'] == '3':
            pass

        elif req['user_flag'] == 4 or req['user_flag'] == '4':
            pass

        elif req['user_flag'] == 5 or req['user_flag'] == '5':
            pass

        else:
            # TODO 其他任务配置，考虑开发一个适配器
            return ''

    def dispatch(self, uid, query):
        intent = intenter.intent_recognition(query)['intent']
        if intent in ['weather', 'play']:
            return 1
        else:
            item = redis_handle.lpop(uid + '.query_history')

            if item:
                item = json.loads(item)
                if item['who'] == 1 or item['who'] == '1':
                    return 1
                else:
                    return 2
            else:
                return 2


if __name__ == '__main__':
    agenter = Agent()
    print(agenter.response({'uid': 'azx', 'user_flag': 1, 'message': {'days': 1, 'departure': '天气'}}))
