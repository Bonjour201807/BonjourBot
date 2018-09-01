"""
@Author: yangdu
@Time: 2018/9/1 下午2:25
@Software: PyCharm
"""
import requests
import json


class Search:
    url = 'http://182.254.227.188:45678/v1/api'
    key = 'B56slIjnkNC0V7QiP3w0OUXdnXBLdhXTEvkVRXnfQNo'

    @classmethod
    def get_tags_by_city(cls,
                         city=None,
                         page=0,
                         size=12):
        url = cls.url + '/tags_by_city'
        payload = {'city': city,
                   'from_page': page,
                   'size': size}
        res = requests.get(url, params=payload)
        print(res.json())

    @classmethod
    def get_tags_by_loc_distance(cls,
                                 loc=None,
                                 distance=None,
                                 page=0,
                                 size=12):
        url = cls.url + '/tags_by_loc_distance'
        payload = {'loc': loc,
                   'distance': distance,
                   'from_page': page,
                   'size': size}
        res = requests.get(url, params=payload)
        print(res.json())

    @classmethod
    def get_tags_by_loc_distance_range(cls,
                                       loc=None,
                                       dismax=None,
                                       dismin=None,
                                       page=0,
                                       size=12):
        url = cls.url + '/tags_by_loc_distance_range'
        payload = {'loc': loc,
                   'dismin': dismin,
                   'dismax': dismax,
                   'from_page': page,
                   'size': size}
        res = requests.get(url, params=payload)
        print(res.json())

    @classmethod
    def get_spots_by_loc_distance_tags(cls,
                                       loc=None,
                                       distance=None,
                                       tags=[],
                                       page=0,
                                       size=3):
        url = cls.url + '/spots_by_loc_distance_tags'
        payload = {'loc': loc,
                   'distance': distance,
                   'from_page': page,
                   'size': size,
                   'tags': json.dumps(tags)}
        res = requests.get(url, params=payload)
        print(res.json())


    @classmethod
    def get_spots_by_loc_distance_tags_range(cls,
                                             loc=None,
                                             dismin=None,
                                             dismax=None,
                                             tags=[],
                                             page=0,
                                             size=3):
        url = cls.url + '/spots_by_loc_distance_tags_range'
        payload = {'loc': loc,
                   'dismin': dismin,
                   'dismax': dismax,
                   'from_page': page,
                   'size': size,
                   'tags': json.dumps(tags)}
        res = requests.get(url, params=payload)
        print(res.json())


if __name__ == '__main__':
    print(Search.get_tags_by_loc_distance(loc='22.543099,114.057868',
                                          distance=100,
                                          page=0))

    print(Search.get_tags_by_loc_distance_range(loc='22.543099,114.057868',
                                                dismin=100,
                                                dismax=200,
                                                page=0))

    print(Search.get_spots_by_loc_distance_tags(loc='22.543099,114.057868',
                                                distance=100,
                                                page=3,
                                                tags=['小镇', '动物', '生态', '观景台', '阳光']))

    print(Search.get_spots_by_loc_distance_tags_range(loc='22.543099,114.057868',
                                                      dismin=100,
                                                      dismax=200,
                                                      page=3,
                                                      tags=['小镇', '动物', '生态', '观景台', '阳光']))

    print(Search.get_tags_by_city(city='成都市',
                                  page=3,
                                  size=3))