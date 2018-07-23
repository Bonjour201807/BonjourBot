from bonjour.nlu.intent_detection.intent_detection import Intent
from bonjour.nlu.slot_filling.slot_filling import SlotFill


class Agent():
    def __init__(self):
        self.Intenter = Intent()
        self.Ner = JNER()
        self.SlotFiller = SlotFill()
        self.Slots = slot1
        self.recorder = []
        #上一轮意图问题
        self.last_question = ""

    def response(self, input):
        intention = self.Intenter.intent_recognition(input)
        # print(intention)
        ner_result = self.Ner.tag(input)
        # print("input:"+input)
        # print("ner_result:"+str(ner_result))
        if intention:
            for item in self.Slots:
                if item["task"] == intention:
                    self.recorder.append(item)

        #临时方案
        if not self.recorder:
            return "助手傻逼了，闭关学习啦"

        # print(ner_result)
        for k in ner_result:
            v = ner_result[k]
            if v:
                for item in self.recorder[0]["slots"]:
                    if item["intent_word"] == k:
                        item["value"] = v
        record = self.recorder[0]
        checked = self.checker(record)
        # print(record)
        if isinstance(checked,dict):
            # slot_result = self.SlotFiller.slotinput_extract()
            self.last_question = checked["question"]
            # print(self.last_question)
            return self.last_question[0]

        if isinstance(checked,list):
            #todo 改成从接口查询
            print("识别结果为：")
            print(self.recorder)
            self.recorder = []
            return "接口还没建设好"

    def checker(self,slot):
        items = slot["slots"]
        tmp = []
        for dct in items:
            if dct["value"]:
                tmp.append(dct)
            else:
                return dct
        return tmp
    #
    # def recorder(self):
    #     pass

