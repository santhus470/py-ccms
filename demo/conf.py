import json

with open('C:\ccms\data_classes\config.json') as f:
    data = json.load(f)
    print(data['brightness'])

