import json
import pprint
import argparse
from sklearn.metrics import log_loss

class CategoryResult:
    def __init__(self, data_dict, pretty_print):
        self.data_dict = data_dict
        self.lang_code = data_dict['lang_code']
        self.category_scores = data_dict['category']

        self.__pretty_print = pretty_print

    def __repr__(self):
        return f'{self.lang_code} {self.category_scores}'

    def __str__(self):
        return self.__pretty_print.pformat(self.data_dict)

def label_from_fasttext(label):
    return label[9:].replace('_', ' ')

def get_log_loss(prediction_dict, category_gt):
    category_gt_dict = {category: 0 for category in prediction_dict.keys()}
    category_gt_dict[category_gt] = 1.0

    y_pred = []
    y_true = []

    for category_name in prediction_dict.keys():
        y_pred.append(prediction_dict[category_name])
        y_true.append(category_gt_dict[category_name])

    return log_loss(y_true, y_pred)

def get_fake_log_loss(num):
    y_pred = [0.0 for i in range(num)]
    y_true = [0.0 for i in range(num)]
    y_true[0] = 1.0
    return log_loss(y_true, y_pred)

categoryTransformDict = {
    'Offers & Promotions': 'Offers & Promotion',
    'Foreign Language Learning': 'Foreign Language Learnin'
}

results_name = '../../outputs/out_cat_{}.txt'
label_name = '../../fastText/data/{}.val'

if __name__ == '__main__':
    categoryList = []

    with open('categories.list', 'r') as f:
        for line in f.readlines():
            categoryList.append(line[:-1])

    parser = argparse.ArgumentParser()
    parser.add_argument('--language', default='en')
    args = parser.parse_args()

    pp = pprint.PrettyPrinter(indent=4)
    categoryResults = []

    with open(results_name.format(args.language), 'r') as f:
        for line in f.readlines():
            data_dict = json.loads(line)

            for category in categoryList:
                if category not in data_dict['category'].keys():
                    data_dict['category'][category] = 0.0

            categoryResult = CategoryResult(data_dict, pp)
            categoryResults.append(categoryResult)

    categoryGroundTruths = []

    with open(label_name.format(args.language), 'r') as f:
        for line in f.readlines():
            words = line.split(' ')
            category = label_from_fasttext(words[0])
            categoryGroundTruths.append(category)

    category_num = len(categoryResults[0].category_scores)
    pred_num = len(categoryResults)
    fake_loss = get_fake_log_loss(category_num)

    success_num = 0
    log_loss_mean = 0.0

    for categoryResult, categoryGroundTruth in zip(categoryResults, categoryGroundTruths):
        if categoryGroundTruth in categoryTransformDict.keys():
            categoryGroundTruth = categoryTransformDict[categoryGroundTruth]

        scores = categoryResult.category_scores
        categoryNow = ''

        if categoryResult.lang_code == args.language:
            log_loss_value = get_log_loss(scores, categoryGroundTruth)

            if len(scores) > 0:
                categoryNow = max(scores, key=scores.get)
        else:
            log_loss_value = fake_loss

        if categoryNow == categoryGroundTruth:
            success_num += 1

        log_loss_mean += log_loss_value / pred_num

    precision_at_1 = success_num / pred_num
    print(f'Precision-at-1: {precision_at_1:.6f}')
    print(f'Log Loss Score: {log_loss_mean:.6f}')
