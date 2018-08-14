#-*-coding:utf-8-*-
"""
@Author: yangdu
@Time: 2018/8/7 下午4:12
@Software: PyCharm
"""
from urllib.request import urlopen
from urllib.parse import urlencode
import re


class LTP:
    def __init__(self):
        self.url_base = "https://api.ltp-cloud.com/analysis/"
        self.patt = re.compile(r'(\[(.*?)\]N.{1})')

    def ner(self, query):
        ner_result = {'PER': [],
                      'ORG': [],
                      'LOC': []}
        ltp_ner_result = self._ner(query)
        patt_result = self.patt.findall(ltp_ner_result)
        for item in patt_result:
            if item[0][-2:] == 'Nh':
                ner_result['PER'].append(item[1].replace(' ', ''))
            elif item[0][-2:] == 'Ns':
                ner_result['LOC'].append(item[1].replace(' ', ''))
            elif item[0][-2:] == 'Ni':
                ner_result['ORG'].append(item[1].replace(' ', ''))

        return ner_result

    def _ner(self, query):
        args = {
            'api_key': 'g2J0d7s4w69hcGgOUvDzYmzmHXxiAq7QkxlE3gCs',
            'text': query,
            'pattern': 'ner',
            'format': 'plain'
        }

        result = urlopen(self.url_base, urlencode(args).encode('utf-8'))

        return result.read().decode()


if __name__ == '__main__':
    ltper = LTP()
    print(ltper.ner('深圳市委'))
