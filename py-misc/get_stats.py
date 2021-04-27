import argparse
from toloka_results import TolokaResults

input_path = '../../results/{}/{}.tsv'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--language", help='The type of language (ar, en, fa, ru, uz).', default='en')
    parser.add_argument("--dataset", help='The name of the first dataset.', default='aggregated_results_pool_23606166__2021_04_26_by_skill')
    args = parser.parse_args()

    input_path_now = input_path.format(args.language, args.dataset)
    tolokaResults = TolokaResults(input_path_now)
    tolokaResults.transform()

    first_cat_counter = {}
    second_cat_counter = {}

    for category in tolokaResults.first_category_dict.full_to_short.keys():
        first_cat_counter[category] = 0

    for category in tolokaResults.second_category_dict.full_to_short.keys():
        second_cat_counter[category] = 0

    for result in tolokaResults.results:
        first_cat_counter[result.category.first] += 1
        second_cat_counter[result.category.second] += 1

    record_num = len(tolokaResults.results)

    for category, count in sorted(first_cat_counter.items(), key=lambda x: x[1], reverse=True):
        print(f'{count / record_num * 100:.4f} % {category} {count}')
    print()

    for category, count in sorted(second_cat_counter.items(), key=lambda x: x[1], reverse=True):
        print(f'{count / record_num * 100:.4f} % {category} {count}')
