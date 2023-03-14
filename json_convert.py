import csv
import json


def converter(csv_file, model):
    with open(csv_file, encoding="UTF-8") as data:
        json_data = []
        for item in csv.DictReader(data):
             del item['id']
             if "price" in item:
                 item['price'] = int (item['price'])

             if "is_published" in item and item["is_published"] == "TRUE":
                 item["is_published"] = True
             elif "is_published" in item and item["is_published"] == "FALSE":
                 item["is_published"] = False

             json_data.append({'model': model, 'fields': item})
        return json_data

def save_file(data, file_name):
    with open(file_name, "w", encoding="UTF-8") as file:
        file.write(json.dumps(data, ensure_ascii=False))

data = converter("data/categories.csv", "ads.category")
save_file(data, "data/categories.json")

data = converter("data/ads.csv", "ads.ad")
save_file(data, "data/ads.json")