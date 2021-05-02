import re
import pprint
import argparse

from data_record import DataRecord

regex_by_lang = {
    'en': r'[^a-z]',
    'ru': r'[^а-яa-z]',
    'uz': r'[^a-zoʻgʻʼ]',
    'ar': r'[^ا-ي]',
    'fa': r'[^\u0600-\u06FF]'
}

def clean_text(text, language):
    return re.sub(' +', ' ', re.sub(regex_by_lang[language], ' ', text.lower())).lstrip().rstrip()

def label_from_fasttext(label):
    return label[9:].replace('_', ' ')

label_name = '../../fastText/data/{}.val'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--language', default='ru')
    parser.add_argument('--dataset_name', default='../../preprocessed/dc0415-input-ru-1k.txt')
    parser.add_argument('--out_dataset_name', default='../../preprocessed/dc0415-input-ru-val.txt')
    args = parser.parse_args()

    pp = pprint.PrettyPrinter(indent=4)
    raw_by_clean_records = {}

    with open(args.dataset_name, 'r') as f:
        for line in f.readlines():
            record = DataRecord(line, pp)
            text = clean_text(str(record), args.language)
            raw_by_clean_records[text] = line

    raw_texts = []

    with open(label_name.format(args.language), 'r') as f:
        for line in f.readlines():
            words = line.split(' ')
            category = label_from_fasttext(words[0])
            text = ' '.join(words[1:])[:-1]

            if text in raw_by_clean_records.keys():
                raw_texts.append(raw_by_clean_records[text])

    with open(args.out_dataset_name, 'w') as f:
        for raw_text in raw_texts:
            f.write(f'{raw_text}')

    print(f'Saved {len(raw_texts)} samples to {args.out_dataset_name}')
