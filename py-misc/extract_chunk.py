import argparse
import numpy as np

input_path = '../../inputs/{}/original/{}-{}.txt'
output_path = '../../preprocessed/{}-{}-{}.txt'

seed_value = 24

if __name__ == '__main__':
    np.random.seed(seed_value)

    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", help='The name of dataset.', default='dc0415-input')
    parser.add_argument("--language", help='The type of language (ar, en, fa, ru, uz).', default='en')
    parser.add_argument("--count", type=int, help='The count of samples.', default=1000)
    parser.add_argument("--prefix", help='The prefix of output file.', default='1k')
    args = parser.parse_args()

    input_path_now = input_path.format(args.dataset, args.dataset, args.language)
    output_path_now = output_path.format(args.dataset, args.language, args.prefix)

    with open(input_path_now, 'r') as f:
        lines = f.readlines()

    random_lines = np.random.choice(lines, args.count)

    with open(output_path_now, 'w') as f:
        for line in random_lines:
            f.write(line)
