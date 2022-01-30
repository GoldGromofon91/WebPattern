import json


class AnalogDB:
    @staticmethod
    def save_in_db(data):
        with open('db.json', 'r', encoding='utf-8') as file:
            data_in_db = json.load(file)
        with open('db.json','w', encoding='utf-8') as f:
            data_in_db.append(data)
            json.dump(data_in_db, f)

