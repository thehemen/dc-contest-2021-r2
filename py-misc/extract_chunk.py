import argparse
import numpy as np

input_path = '../../inputs/{0}/{1}/{0}-{2}{3}.txt'
output_path = '../../preprocessed/{0}-{1}-{2}{3}.txt'

seed_value = 24

if __name__ == '__main__':
    np.random.seed(seed_value)

    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", help='The name of dataset.', default='dc-concat')
    parser.add_argument("--language", help='The type of language (ar, en, fa, ru, uz).', default='uz')
    parser.add_argument("--translation", help='The type of translation (original, translated).', default='original')
    parser.add_argument("--count", type=int, help='The count of samples.', default=1000)
    parser.add_argument("--prefix", help='The prefix of output file.', default='1k')
    args = parser.parse_args()

    translation_prefix = '-translated' if args.translation == 'translated' else ''

    input_path_now = input_path.format(args.dataset, args.translation, args.language, translation_prefix)
    output_path_now = output_path.format(args.dataset, args.language, args.prefix, translation_prefix)

    with open(input_path_now, 'r') as f:
        lines = f.readlines()

    random_lines = np.random.choice(lines, args.count)

    with open(output_path_now, 'w') as f:
        for line in random_lines:
            f.write(line)
