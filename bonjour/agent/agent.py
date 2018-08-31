"""
@Author: yangdu
@Time: 2018/8/4 下午5:27
@Software: PyCharm
"""

from bonjour.agent.run_task import RunTask
from bonjour.utils import logger
from bonjour.agent.amap_api import Amap
from bonjour.utils.common_utils import *
from bonjour.agent.es_api import *
from bonjour.utils.db_utils import redis_handle


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
            req_dct['uid'] = req['uid']
            req_dct['query'] = req['message']['query']
            #logger.debug('angent.response,{}'.format(self._task_runner.run(req_dct)))
            return self._task_runner.run(req_dct)

        elif req['user_flag'] == 1 or req['user_flag'] == '1':
            distance = cvt_days(req['message']['days'])
            loc = Amap.geocode(req['message']['departure'])
            if distance and loc:
                redis_handle.set(req['uid']+':info', {'distance': distance, 'loc': loc})
                return search_tags(uid=req['uid'], loc=loc, distance=distance)
            else:
                return None

        elif req['user_flag'] == 2 or req['user_flag'] == '2':
            user_info = eval(redis_handle.get(req['uid']+':info'))
            tags = req['message']['select_tags'] + req['message']['input_tags']
            scroll_id = req.get('scroll_id')
            return search_attractions(loc=user_info['loc'], distance=user_info['distance'], tags=tags, scroll_id=scroll_id)

        elif req['user_flag'] == 3 or req['user_flag'] == '3':
            pass

        elif req['user_flag'] == 4 or req['user_flag'] == '4':
            pass

        elif req['user_flag'] == 5 or req['user_flag'] == '5':
            pass

        else:
            # TODO 其他任务配置，考虑开发一个适配器
            return ''


if __name__ == '__main__':
    agenter = Agent()
    print(agenter.response({'uid':'azx','user_flag':1,'message':{'days':1,'departure':'乌鲁木齐市'}}))