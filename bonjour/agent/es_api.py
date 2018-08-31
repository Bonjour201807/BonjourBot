"""
@Author: yangdu
@Time: 2018/8/28 下午3:59
@Software: PyCharm
"""
from bonjour.utils.db_utils import redis_handle
from elasticsearch import Elasticsearch

ES = Elasticsearch()


def tags_scroll(uid, scroll_id):
    return search_tags(uid=uid, scroll_id=scroll_id)


def attractions_scroll(scroll_id, uid=None):
    return search_attractions(scroll_id=scroll_id)


def search_tags(uid=None, scroll_id=0, scroll_size=12, loc=None, distance=None):
    if isinstance(scroll_id,str):
        scroll_id = eval(scroll_id)
    uid_tag = uid + ':tag'
    if scroll_id == 0:
        tags = []
        res = search_by_distance(loc=loc, distance=distance, size=100)
        print(res)
        for item in res['hits']['hits']:
            for tag in item['_source']['tags']:
                tags.append(tag)
        for tag in set(tags):
            redis_handle.rpush(uid_tag, tag)
        tags = redis_handle.lrange(uid_tag, scroll_id, scroll_id+scroll_size-1)
        tags = [tag for tag in tags]
        return {'flag': 2,
                'message': {
                        'scroll_id': scroll_id+scroll_size,
                        'text': '您可能感兴趣的标签：',
                        'tags': tags}}
    else:
        tags = redis_handle.lrange(uid_tag, scroll_id, scroll_id+scroll_size-1)
        tags = [tag for tag in tags]
        if tags:
            return {'flag': 2,
                    'message': {
                        'scroll_id': scroll_id+scroll_size,
                        'text': '您可能感兴趣的标签：',
                        'tags': tags}}
        else:

            return {'flag': 2,
                    #'scroll_id': scroll_id-scroll_size,
                    'message': {
                        'scroll_id': scroll_id-scroll_size,
                        'text': '您可能感兴趣的标签：',
                        'tags': ["云海", "湖泊", "雪山", "日出", "冰川", "峡谷"]}}


def search_attractions(loc=None, distance='100km', tags=None, scroll_id=None, size=3):
    if not scroll_id:
        res = search_by_distance(loc, distance, tags, scroll='2m', size=size)
        scroll_id = res['_scroll_id']
        data = res['hits']['hits']
        data = [item['_source'] for item in data]
        for item in data:
            item['pic_path'] = item['images']
        return {
                'flag': 3,
                'message': {'data':data,
                            'scroll_id': scroll_id}}
    else:
        res = ES.scroll(scroll_id=scroll_id, scroll='2m')
        scroll_id = res['_scroll_id']
        data = res['hits']['hits']
        data = [item['_source'] for item in data]
        for item in data:
            item['pic_path'] = item['images']
        ret = {'flag': 3,
               'message': {'data':data,
                           'scroll_id':scroll_id}}
        return ret


def search_by_distance(loc, distance='100km', tags=None, scroll=None, size=3):
    """
    计算以loc为中心的distance距离范围内的点
    :param loc: 字典{"lat":48.658992,"lon":87.040846}或者数组[lon, lat]或字符串"lat,lon" note:后两种形式lon和lat前后相反
    :param distance:
    :return:
    """
    should_terms = []
    if tags:
        for tag in tags:
            tag_dict = [{'match': {'name': tag}},
                        {'match': {'summary': tag}}]
            should_terms.extend(tag_dict)

    geo_dict = {"geo_distance":
                    {"distance": distance, "loc": loc}}

    body = {
        "query": {
            "bool": {
                "filter": geo_dict,
                'should': should_terms
            }
        }
    }

    if scroll:
        res = ES.search(index='bonjour', doc_type='attractions', body=body, size=size,scroll='2m')
    else:
        # res = ES.search(index='bonjour', doc_type='attractions', body=body, size=50, from_=offset)
        res = ES.search(index='bonjour', doc_type='attractions', body=body, size=size)

    return res


def search_by_distance_range(loc, gte_distance, lt_distance, offset=0):
    res_big = search_by_distance(loc, lt_distance, offset=offset)
    res_small = search_by_distance(loc, gte_distance, offset=offset)
    return [item for item in res_big if item not in res_small]


if __name__ == '__main__':
    # 114.057868, 22.543099
    # res = search_by_distance([87.040846, 48.658992], '10km')
    # res = search_by_distance(','.join([str(48.658992), str(87.040846)]), '10km')
    print(search_tags(uid='zxcv1', loc='22.543099,114.057868',distance='0.1km'))
    print(tags_scroll(uid='zxcv1', scroll_id=12))
    res = search_attractions('22.543099,114.057868', '100km',tags=['林', '栈道', '青山', '牧场', '船', '小镇', '动物', '生态', '观景台', '阳光'])
    print(res)
    print(attractions_scroll(scroll_id='DnF1ZXJ5VGhlbkZldGNoBQAAAAAAAMCNFmRFTXFFYW84VHpTWWtMSWpaNTd2bXcAAAAAAADAjBZkRU1xRWFvOFR6U1lrTElqWjU3dm13AAAAAAAAwI4WZEVNcUVhbzhUelNZa0xJalo1N3ZtdwAAAAAAAMCPFmRFTXFFYW84VHpTWWtMSWpaNTd2bXcAAAAAAADAkBZkRU1xRWFvOFR6U1lrTElqWjU3dm13'))
    print('-------')
    # res1 = search_by_distance({"lat": 48.658992, "lon": 87.040846}, '30km')
    # print(len(res1), res1)
    # print('-------')
    # res2 = search_by_distance_range({"lat" : 48.658992, "lon" : 87.040846}, '20km','30km')
    # print(len(res2), res2)
    # print('-------')

