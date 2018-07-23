import yaml
import re


class Intent:
    def __init__(self, intent_path='./data/intent/intent.yaml'):
        #临时方案
        self.rule_intent_map = {}
        with open(intent_path, encoding='utf8') as f:
            intent_dict = yaml.load(f)
            intent_keys = intent_dict['intent'].keys()
            for intent in intent_keys:
                for rule_expr in intent_dict['intent'][intent]:
                    self.rule_intent_map[re.compile(rule_expr)] = intent

    def intent_recognition(self, query):
        #临时方案
        intent_map = {'intent': ''}
        for rule_expr, intent_word in self.rule_intent_map.items():
            if rule_expr.search(query):
                intent_map['intent'] = intent_word
                return intent_map
        return intent_map


if __name__ == '__main__':
    import sys
    sys.path.append('/Users/dy/Desktop/back/InfoR/bonjour')
    intent_haddle = Intent('/Users/dy/Desktop/back/InfoR/bonjour/data/intent/intent.yaml')
    print(intent_haddle.intent_recognition('我想出去玩'))