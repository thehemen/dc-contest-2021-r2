import re
import json
import pprint
import argparse
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

from data_record import DataRecord

regex_by_lang = {
    'en': r'[^a-z]',
    'ru': r'[^а-яa-z]',
    'uz': r'[^a-zoʻgʻʼ]',
    'ar': r'[^ا-ي]'
}

def clean_text(text, language):
    return re.sub(' +', ' ', re.sub(regex_by_lang[language], ' ', text.lower())).lstrip().rstrip()

def save_dataset(path, X, y):
    with open(path, 'w') as f:
        for text, category in zip(X, y):
            f.write(f'{category} {text}\n')

    print(f'Saved {len(X)} samples to {path}')

def label_to_fasttext(label):
    return '__label__' + label.replace(' ', '_')

def label_from_fasttext(label):
    return label[9:].replace('_', ' ')


if __name__ == '__main__':
    with open('categories.json', 'r') as f:
        category_dict = json.load(f)

    parser = argparse.ArgumentParser()
    parser.add_argument('--language', default='ar')
    parser.add_argument('--dataset_name', default='../../preprocessed/dc-concat-ar-1k.txt')
    parser.add_argument('--log_name', default='../../outputs/dc-concat-ar-1k-ground-truth.txt')
    parser.add_argument('--out_label_name', default='../../fastText/data/{}.{}')
    args = parser.parse_args()

    pp = pprint.PrettyPrinter(indent=4)
    records = []

    with open(args.dataset_name, 'r') as f:
        for line in f.readlines():
            dataRecord = DataRecord(line, pp)
            records.append(dataRecord)

    category_by_idx = {}

    with open(args.log_name, 'r') as f:
        for line in f.readlines():
            idx = int(line.split(' ')[0])
            category = ' '.join([x for x in line.split(' ')[1:]])[:-1]
            category_by_idx[idx] = category

    X, y = [], []

    for idx, record in enumerate(records):
        if idx not in category_by_idx.keys():
            continue

        text = clean_text(str(record), args.language)
        category = category_by_idx[idx]
        category_fasttext = label_to_fasttext(category)
        X.append(text)
        y.append(category_fasttext)

    X_train, X_test, y_train, y_test = train_test_split(X, y,
        test_size=0.15, random_state=42)

    save_dataset(args.out_label_name.format(args.language, 'train'), X_train, y_train)
    save_dataset(args.out_label_name.format(args.language, 'val'), X_test, y_test)

    category_count = {}

    for meta_category, categories in category_dict.items():
        for category in categories:
            train_count = [label_from_fasttext(y) for y in y_train].count(category)
            val_count = [label_from_fasttext(y) for y in y_test].count(category)

            category_count[category] = {}
            category_count[category]['train'] = train_count
            category_count[category]['val'] = val_count

    max_count = max([max([v['train'], v['val']]) for k, v in category_count.items()])
    cx, cy_train, cy_test = [], [], []

    for category, count in sorted(category_count.items(), key=lambda x: x[1]['train'] + x[1]['val'], reverse=True):
        cx.append(category)
        cy_train.append(count['train'])
        cy_test.append(count['val'])

    fig, ax = plt.subplots()
    ax.barh(cx, cy_test, color='red')
    ax.barh(cx, cy_train, color='blue', left=cy_test)
    ax.set_title(args.log_name.split('/')[-1])
    ax.set_xlim([0, max_count])
    plt.show()
