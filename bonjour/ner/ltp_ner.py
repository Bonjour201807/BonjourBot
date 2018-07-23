import os

from pyltp import Postagger
from pyltp import Segmentor
from pyltp import NamedEntityRecognizer


class LTP:
    def __init__(self,
                 ltp_data_path=None,
                 seg_lexicon=None,
                 pos_lexicon=None,
                 ):
        if not ltp_data_path:
            raise ValueError('请指定ltp用到的模型所在路径！！！')

        self.ltp_data_path = ltp_data_path  # ltp模型目录的路径
        self._cws_model_path = os.path.join(self.ltp_data_path, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
        self._pos_model_path = os.path.join(self.ltp_data_path, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
        self._ner_model_path = os.path.join(self.ltp_data_path, 'ner.model')  # 命名实体识别模型路径，模型名称为`pos.model`

        self._segmentor = Segmentor()  # 初始化实例
        if seg_lexicon:
            self._segmentor.load_with_lexicon(self._cws_model_path, seg_lexicon)  # 加载模型，第二个参数是您的外部词典文件路径
        else:
            self._segmentor.load(self._cws_model_path)

        self._postagger = Postagger()  # 初始化实例
        if pos_lexicon:
            self._postagger.load_with_lexicon(self._pos_model_path, pos_lexicon)  # 加载模型，第二个参数是您的外部词典文件路径
        else:
            self._postagger.load(self._pos_model_path)

        self._recognizer = NamedEntityRecognizer()  # 初始化实例
        self._recognizer.load(self._ner_model_path)  # 加载模型

    def cut(self, text):
        return self._segmentor.segment(text)

    def pos(self, text):
        words = self.cut(text)
        postags = self._postagger.postag(words)

        return zip(words, postags)

    def ner(self, text):
        """
        命名实体识别，提供三种命名识别，PER人名、LOC地名、ORG机构名
        :param text:
        :return:
        """
        # Nh代表人名, Ni代表机构名，Ns代表地点名字
        ner_dict = {'Nh': [],
                    'Ni': [],
                    'Ns': []}
        words = self.cut(text)
        postags = self._postagger.postag(words)
        nertags = self._recognizer.recognize(words, postags)

        ner_tmp = []
        for i, tag in enumerate(nertags):
            if tag == 'O':
                continue
            if tag.startswith('S'):
                tag = tag.split('-')[-1]
                ner_dict[tag].append(words[i])
            elif tag.startswith('B') or tag.startswith('I'):
                ner_tmp.append(words[i])
                continue
            elif tag.startswith('E'):
                ner_tmp.append(words[i])
                tag = tag.split('-')[-1]
                ner_dict[tag].append(''.join(ner_tmp))
                ner_tmp = []
        if ner_tmp:
            tag = list(nertags)[-1]
            tag = tag = tag.split('-')[-1]
            ner_dict[tag].append(''.join(ner_tmp))

        ner_map = dict()
        ner_map['PER'] = ner_dict['Nh']
        ner_map['ORG'] = ner_dict['Ni']
        ner_map['LOC'] = ner_dict['Ns']

        return ner_map

    def release(self):
        self._postagger.release()


if __name__ == '__main__':
    ltp_haddle = LTP(
        ltp_data_path='/Users/dy/Desktop/back/InfoR/bonjour/data/ltp/ltp_data_v3.4.0'
    )
    text = '我正在去清华大学深圳研究院'
    print(list(ltp_haddle.cut(text)))
    print(list(ltp_haddle.pos(text)))
    print(ltp_haddle.ner(text))
