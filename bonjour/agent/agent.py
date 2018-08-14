"""
@Author: yangdu
@Time: 2018/8/4 下午5:27
@Software: PyCharm
"""

from bonjour.agent.run_task import RunTask
from bonjour.utils import logger


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
            logger.debug('angent.response,{}'.format(self._task_runner.run(req_dct)))
            return self._task_runner.run(req_dct)
        else:
            # TODO 其他任务配置，考虑开发一个适配器
            return ''
