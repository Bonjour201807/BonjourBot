"""
@Author: yangdu
@Time: 2018/8/4 下午5:27
@Software: PyCharm
"""

from bonjour.nlu.slot_filling.slot_filling import SlotFilling
from bonjour.nlu.intent_detection.intent_detection import Intent


class NLU:
    def __init__(self):
        self.intent_haddle = Intent()
        self.slot_fill_haddle = SlotFilling()

    def nlu(self, query: str) -> dict:
        intent = self.intent_haddle.intent_recognition(query)
        slot_value = self.slot_fill_haddle.slot_extract(query)

        return {**intent, **slot_value}


if __name__ == '__main__':
    nlu_handle = NLU()
    nlu_handle.nlu('帮我查下南山区的天气')
