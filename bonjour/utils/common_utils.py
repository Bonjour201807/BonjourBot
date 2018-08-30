
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
