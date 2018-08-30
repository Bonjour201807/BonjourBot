"""
@Author: yangdu
@Time: 2018/8/30 下午1:50
@Software: PyCharm
"""
import requests


class Amap():
    geocode_url = 'https://restapi.amap.com/v3/geocode/geo'
    key = '786ab5706d27e723044f572e0f739acc'

    @classmethod
    def geocode(cls, address):
        body = {'key': cls.key, 'address': address}
        res = requests.get(cls.geocode_url, params=body).json()
        if res['count']=='0' or res['count']==0:
            return None
        else:
            loc = res['geocodes'][0]['location']
            loc = ','.join(loc.split(',')[::-1])
            return loc


if __name__ == '__main__':
    print(Amap.geocode('天津市'))

