# from bonjour.ner.jner import JNER
from bonjour.ner.ltp_ner import LTP
from bonjour.ner.time_extract import TimeExtract


class SlotFilling:
    def __init__(self, ltp_data_path='./data/ltp/ltp_data_v3.4.0'):
        self._ltp_handle = LTP(ltp_data_path=ltp_data_path)
        self._time_extract = TimeExtract()

    def slot_extract(self, query):
        """
        槽位抽取
        :param query:
        :return:
        """
        std_ner_result = self._ltp_handle.ner(query)
        time_ner_result = self._time_extract.extract(query)
        slot_dict = {**std_ner_result, **time_ner_result}
        slot_keys = list(slot_dict.keys())
        for k in slot_keys:
            if not slot_dict[k]:
                del slot_dict[k]

        return {'slot': slot_dict}


if __name__ == '__main__':
    slot_fill = SlotFilling(ltp_data_path='/Users/dy/Desktop/back/InfoR/bonjour/data/ltp/ltp_data_v3.4.0')
    print(slot_fill.slot_extract('我想问下明后中午12点天龙岗的天气？'))
