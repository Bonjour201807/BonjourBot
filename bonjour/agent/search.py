"""
@Author: yangdu
@Time: 2018/9/1 下午5:26
@Software: PyCharm
"""

from bonjour.agent.search_api import Search
from bonjour.utils.db_helper import redis_handle
from bonjour.utils.utils import cvt_days
from bonjour.agent.amap_api import Amap


def spots_scroll(req):
    uid = req['uid']
    from_page = req['from_page']
    size = req['size']
    if isinstance(from_page, str):
        from_page = int(from_page)
    if isinstance(size, int):
        size = int(size)
    loc = Amap.geocode(req['data']['departure'])
    distance = cvt_days(req['data']['days'])
    tags = req['data']['select_tags']+[req['data']['input_tag']]

    res = Search.get_spots_by_loc_distance_tags(loc=loc,
                                                distance=distance,
                                                tags=tags,
                                                page=from_page*size,
                                                size=size)
    ret = {'message': res}

    return ret


def tags_scroll(req):
    uid = req['uid']
    from_page = req['from_page']
    size = req['size']
    if isinstance(from_page, str):
        from_page = int(from_page)
    if isinstance(size, int):
        size = int(size)
    loc = Amap.geocode(req['data']['departure'])
    distance = cvt_days(req['data']['days'])

    res = Search.get_tags_by_loc_distance(loc=loc,
                                          distance=distance,
                                          page=from_page * size,
                                          size=size)
    ret = {'message': res}

    return ret

