import json


def read_json(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        return json.load(f)


if __name__=="__main__":
    data = read_json('data.json')
    print(data[7])