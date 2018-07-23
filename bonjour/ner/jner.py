import jieba
import jieba.posseg as psg


class JNER():
    def __init__(self):
        self.ner_tags = {"time":"how_many_days","place":"from_place"}
        jieba.load_userdict("./data/dict/ner.txt")

    def tag(self, query):
        tag_dict = {}
        # for k in self.ner_tags:
        #     tag_dict[self.ner_tags[k]]=""
        tagged = [(word, flag) for word, flag in psg.cut(query)]
        # print(str(tagged))
        for item in tagged:
            if item[1] in self.ner_tags:
                tag_dict[self.ner_tags[item[1]]] = item[0]

        return tag_dict
