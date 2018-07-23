# -*- coding:utf-8 -*-
import json
from bonjour.ner.time_ner.TimeNormalizer import TimeNormalizer


class TimeExtract():
    def __init__(self):
        self._time_extracter = TimeNormalizer()

    def extract(self, query):
        time_result = self._time_extracter.parse(query)

        if 'error' in time_result:
            return {'time': ''}
        else:
            time_result = json.loads(time_result,encoding='utf8')
            if time_result['type'] == 'timestamp':
                return {'time': time_result['timestamp']}
            if time_result['type'] == 'time':
                return {'time': time_result['timestamp'][0]}


if __name__ == '__main__':
    time_extracter = TimeExtract()
    print(time_extracter.extract('我想知道两天后的天气？'))

