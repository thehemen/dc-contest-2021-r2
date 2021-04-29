import re
import pprint
import argparse
from sklearn.model_selection import train_test_split

from data_record import DataRecord

regex_by_lang = {
    'en': r'[^a-z]',
    'ru': r'[^а-я]'
}

def clean_text(text, language):
    return re.sub(' +', ' ', re.sub(regex_by_lang[language], ' ', text.lower())).lstrip().rstrip()

def save_dataset(path, X, y):
    with open(path, 'w') as f:
        for text, category in zip(X, y):
            f.write(f'{category} {text}\n')

    print(f'Saved {len(X)} samples to {path}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--language', default='en')
    parser.add_argument('--dataset_name', default='../../preprocessed/dc0415-input-en-2k.txt')
    parser.add_argument('--log_name', default='../../outputs/dc0415-en-2k-ground-truth.txt')
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
        category_fasttext = '__label__' + category.replace(' ', '_')
        X.append(text)
        y.append(category_fasttext)

    X_train, X_test, y_train, y_test = train_test_split(X, y,
        test_size=0.15, random_state=42)

    save_dataset(args.out_label_name.format(args.language, 'train'), X_train, y_train)
    save_dataset(args.out_label_name.format(args.language, 'val'), X_test, y_test)
