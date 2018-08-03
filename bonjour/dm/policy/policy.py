import json
import yaml
import random

from bonjour.dm.dst.dst import DST, redis_handle


class Policy:
    def __init__(self):
        self.dst_handle = DST()

        # 临时方案，要改成配置文件
        self.policy_tree = yaml.load(open('/Users/pangyuming/Downloads/BonjourBot/data/intent/intent_questions.yaml'))

    def ploicy(self, request):
        self.dst_handle.dst(request)
        uid = request['uid']
        uid_intent = '{}:intent'.format(uid)
        for item in redis_handle.lrange(uid_intent, 0, -1):
            item = json.loads(item)
            if item['state'] == 1:
                is_has_none = self._has_none(item['slot'])
                # print('is_has_none...', is_has_none)
                if not is_has_none:
                    return {'answer': item,
                            'question': '',
                            'tag': 1,
                            'intent': item['intent']}
                else:
                    slot_dct=self.policy_tree[item['intent']]
                    for slot, questions in slot_dct.items():
                        if slot in is_has_none:
                            question = random.choice(questions)
                            return {'answer': '',
                                    'question': question,
                                    'tag': 0,
                                    'intent': item['intent']}
            else:
                continue

    def _has_none(self, dct):
        """
        检查一个字典是否有value为None
        :param dct:
        :return:
        """
        none_keys = []
        for k, v in dct.items():
            if (not v) or v=='None':
                none_keys.append(k)
        if none_keys:
            return none_keys
        else:
            return None