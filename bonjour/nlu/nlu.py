"""
@Author: yangdu
@Time: 2018/8/4 下午5:27
@Software: PyCharm
"""

from bonjour.nlu.intent_detection import Intent
from bonjour.nlu.slot_filling import SlotFilling


class NLU:
    def __init__(self):
        self.intent_handle = Intent()
        self.slot_fill_handle = SlotFilling()

    def nlu(self, query: str) -> dict:
        intent = self.intent_handle.intent_recognition(query)
        slot_value = self.slot_fill_handle.slot_extract(query)

        return {**intent, **slot_value}


if __name__ == '__main__':
    nlu_handle = NLU()
    print(nlu_handle.nlu('帮我查下南山区的天气'))
