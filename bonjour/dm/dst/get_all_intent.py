import yaml


# 临时方案
with open('all_intent.yaml', encoding='utf8') as f:
    intent = yaml.load(f)
    print(intent)