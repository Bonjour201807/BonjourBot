
def cvt_days(days):

    if isinstance(days, float) or isinstance(days, int):
        distance = str(days*100)+'km'
        return distance

    else:
        try:
            days = eval(days)
            distance = str(days * 100) + 'km'
            return distance
        except:
            return None


#装饰器方法加入单例模式
def singleton(cls):
    instances = {}

    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper


#使用基类加入单例模式
class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance


def has_none(dct):
    """
    检查一个字典是否有value为None
    :param dct:
    :return:
    """
    none_keys = []
    for k, v in dct.items():
        if (not v) or v == 'None':
            none_keys.append(k)
    if none_keys:
        return none_keys
    else:
        return None
