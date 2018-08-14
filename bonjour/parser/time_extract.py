# -*- coding:utf-8 -*-
"""
@Author: yangdu
@Time: 2018/8/4 下午5:27
@Software: PyCharm
"""

import json
import datetime

from dateutil import parser
from bonjour.utils import logger
from bonjour.parser.time_ner.TimeNormalizer import TimeNormalizer


class TimeExtract:
    def __init__(self):
        self._time_extracter = TimeNormalizer()

    def extract(self, query):
        time_result = self._time_extracter.parse(query)
        geted_time = {'start_time': None, 'delta_time': None}

        if 'error' in time_result:
            return geted_time

        else:
            time_result = json.loads(time_result, encoding='utf8')
            if time_result['type'] == 'timestamp':
                geted_time['delta_time'] = str(datetime.timedelta(days=1))
                geted_time['start_time'] = time_result['timestamp']
                logger.debug('time,{}'.format(geted_time))
                return geted_time

            elif time_result['type'] == 'timespan':
                timedelta = parser.parse(time_result['timespan'][1]) - parser.parse(time_result['timespan'][0])
                geted_time['delta_time'] = timedelta
                geted_time['start_time'] = time_result['timespan'][0]
                logger.debug('time,',geted_time)
                return geted_time

            elif time_result['type'] == 'timedelta':
                time_start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                geted_time['delta_time'] = time_result['timedelta']
                geted_time['start_time'] = time_start
                logger.debug('time',geted_time)
                return geted_time
        return geted_time


if __name__ == '__main__':
    time_extracter = TimeExtract()
    print(time_extracter.extract('我想知道一个明天的天气？'))

