import csv
import json

class Category:
    def __init__(self, first, second, confidence=1.0):
        self.first = first
        self.second = second
        self.confidence = confidence

    def __repr__(self):
        return f'{self.first} {self.second} {self.confidence:.6f}'

class TolokaResult:
    def __init__(self, row):
        self.task_id = row[0]
        self.text = row[1]
        self.category = Category(row[2], row[3], float(row[4][:-1]) / 100.)
        self.category_gt = Category(row[5], row[6])

class CategoryDict:
    def __init__(self, full_to_short, short_to_full):
        self.full_to_short = full_to_short
        self.short_to_full = short_to_full

class TolokaResults:
    first_category_path = 'first_cat_dict.json'
    second_category_path = 'second_cat_dict.json'

    def __init__(self, path):
        self.results = []

        with open(path, 'r', newline='\n') as f:
            reader = csv.reader(f, delimiter='\t')

            for i, row in enumerate(reader):
                if i == 0:
                    continue

                self.results.append(TolokaResult(row))

        self.first_category_dict = self.__read_category_dict(self.first_category_path)
        self.second_category_dict = self.__read_category_dict(self.second_category_path)

    def transform(self):
        for i, result in enumerate(self.results):
            self.results[i].category.first = self.__transform_category(result.category.first, self.first_category_dict)
            self.results[i].category.second = self.__transform_category(result.category.second, self.second_category_dict)
            self.results[i].category_gt.first = self.__transform_category(result.category.first, self.first_category_dict)
            self.results[i].category_gt.second = self.__transform_category(result.category.second, self.second_category_dict)

    def __transform_category(self, category, category_dict):
        if category in category_dict.full_to_short.keys():
            category = category_dict.full_to_short[category]

        elif category in category_dict.short_to_full.keys():
            category = category_dict.short_to_full[category]

        return category

    def __read_category_dict(self, category_path):
        with open(category_path, 'r') as f:
            full_to_short = json.load(f)

        short_to_full = {}

        for k, v in full_to_short.items():
            short_to_full[v] = k

        return CategoryDict(full_to_short, short_to_full)
