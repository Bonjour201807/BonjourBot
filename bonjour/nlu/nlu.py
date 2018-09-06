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

    def parse(self, query: str) -> dict:
        intent = self.intent_handle.intent_recognition(query)
        slot_value = self.slot_fill_handle.slot_extract(query)

        # type==0表示从文本抽取， type==1表示从前端表单获取
        return {**intent, **slot_value}


if __name__ == '__main__':
    nlu_handle = NLU()
    print(nlu_handle.nlu('nihao'))
    print(1 if nlu_handle.nlu('nihao')['intent'] else 0)
    print(1 if nlu_handle.nlu('nihao')['slot'] else 0)
