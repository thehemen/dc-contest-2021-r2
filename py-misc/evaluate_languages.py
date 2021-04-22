import tqdm
import pprint
import argparse

from data_record import DataRecord
from result_record import ResultRecord

input_path = '../../inputs/{}/original/dc0415-input-{}.txt'
lang_path = '../../inputs/{}/original/dc0415-input-{}.txt'
output_path = '../../outputs/out_{}.txt'
languages = ['ar', 'en', 'fa', 'ru', 'uz']

log_path = '../../outputs/log.txt'

EPS = 1e-9

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", help='The name of dataset.', default='dc0415-input')
    parser.add_argument("--language", help='The type of language (ar, en, fa, ru, uz, all).', default='all')
    args = parser.parse_args()

    arg_dataset = args.dataset
    arg_language = args.language

    input_path_now = input_path.format(arg_dataset, arg_language)
    output_path_now = output_path.format(arg_language)

    if arg_language in languages:
        languages = [arg_language]

    print(input_path_now)
    print(output_path_now)
    print(languages)

    records, results = [], []

    records_id_by_hash = {}
    pp = pprint.PrettyPrinter(indent=4)

    with open(input_path_now, 'r') as f:
        lines = f.readlines()

        for i in tqdm.tqdm(range(len(lines))):
            record = DataRecord(lines[i], pp)
            hash_value = hash(record)
            records.append(record)
            records_id_by_hash[hash_value] = i

    for i in tqdm.tqdm(range(len(languages))):
        lang_code = languages[i]
        lang_path_now = lang_path.format(arg_dataset, lang_code)

        with open(lang_path_now, 'r') as f:
            lines = f.readlines()

            for line in lines:
                record = DataRecord(line, pp)
                hash_value = hash(record)

                if hash_value in records_id_by_hash.keys():
                    records[records_id_by_hash[hash_value]].lang_code = lang_code

    with open(output_path_now, 'r') as f:
        lines = f.readlines()

        for line in lines:
            result = ResultRecord(line, pp)
            results.append(result)

    lang_stats = {x: {'FP': 0, 'FN': 0, 'TP': 0} for x in languages}

    for record, result in zip(records, results):
        lang_code_true = record.lang_code
        lang_code_predicted = result.lang_code

        if lang_code_true == lang_code_predicted:
            if lang_code_true in languages:
                lang_stats[lang_code_true]['TP'] += 1
        else:
            if lang_code_true in languages:
                lang_stats[lang_code_true]['FN'] += 1

            if lang_code_predicted in languages:
                lang_stats[lang_code_predicted]['FP'] += 1

    F1_scores = []

    for language in lang_stats.keys():
        lang_stats_now = lang_stats[language]
        FP = lang_stats_now['FP']
        FN = lang_stats_now['FN']
        TP = lang_stats_now['TP']

        precision = TP / (TP + FP + EPS)
        recall = TP / (TP + FN + EPS)
        F1 = 2 * precision * recall / (precision + recall + EPS)
        F1_scores.append(F1)

        print(f'\n{language}')
        print(f'True Positive: {TP}')
        print(f'False Positive: {FP}')
        print(f'False Negative: {FN}')
        print(f'Precision: {precision:.3f}')
        print(f'Recall: {recall:.3f}')
        print(f'F1: {F1:.3f}')

    with open(log_path, 'a') as f:
        for F1 in F1_scores:
            f.write(f'{F1:.3f}\t'.replace('.', ','))
        f.write(f'\n')
