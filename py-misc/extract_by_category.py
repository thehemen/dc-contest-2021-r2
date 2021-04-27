import argparse
from toloka_results import TolokaResults

input_path = '../../results/{}/{}.tsv'
output_path = '../../results/{}/categories/{}/{}.txt'

def write_category_texts(tag, language, category_texts):
    for category, texts in category_texts.items():
        with open(output_path.format(language, tag, category), 'w') as f:
            for text in texts:
                f.write(f'{text}\n\n\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--language", help='The type of language (ar, en, fa, ru, uz).', default='en')
    parser.add_argument("--dataset", help='The name of the first dataset.', default='aggregated_results_pool_23606166__2021_04_26_by_skill')
    args = parser.parse_args()

    input_path_now = input_path.format(args.language, args.dataset)
    tolokaResults = TolokaResults(input_path_now)
    tolokaResults.transform()

    first_category_texts = {}
    second_category_texts = {}

    for category in tolokaResults.first_category_dict.full_to_short.keys():
        first_category_texts[category] = []

    for category in tolokaResults.second_category_dict.full_to_short.keys():
        second_category_texts[category] = []

    for result in tolokaResults.results:
        text = result.text
        first_category_texts[result.category.first].append(text)
        second_category_texts[result.category.second].append(text)

    write_category_texts('first', args.language, first_category_texts)
    write_category_texts('second', args.language, second_category_texts)
