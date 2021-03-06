from bonjour.utils import Singleton
from bonjour.parser import LTP, TimeExtract


class SlotFilling(Singleton):
    def __init__(self):
        self._ltp_handle = LTP()
        self._time_extract = TimeExtract()

    def slot_extract(self, query):
        """
        槽位抽取
        :param query:
        :return:
        """
        # query后面加个呢字，为了解决ltp把地名识别成机构名字
        query = query.strip()+'呢'
        std_ner_result = self._ltp_handle.ner(query)
        time_ner_result = self._time_extract.extract(query)
        slot_dict = {**std_ner_result, **time_ner_result}
        slot_keys = list(slot_dict.keys())
        for k in slot_keys:
            if not slot_dict[k]:
                del slot_dict[k]

        return {'slot': slot_dict}


if __name__ == '__main__':
    slot_fill = SlotFilling()
    print(slot_fill.slot_extract('我想问下明后中午12点天龙岗的天气？'))
