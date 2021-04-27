import csv
import numpy as np
import argparse

seed_value = 35
input_path = '../../inputs-outputs/{}-{}-{}.tsv'

def read_tsv(path):
    lines = []

    with open(path, 'r', newline='\n') as f:
        reader = csv.reader(f, delimiter='\t')

        for line in reader:
            lines.append(line[0])

    return lines

if __name__ == '__main__':
    np.random.seed(seed_value)

    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", help='The name of the first dataset.', default='dc0415-dc0421-input')
    parser.add_argument("--language", help='The type of language (ar, en, fa, ru, uz).', default='en')
    parser.add_argument("--length", help='The number of rows to be extracted', type=int, default=30)
    parser.add_argument("--prefix_input", help='The prefix of input file.', default='2k')
    parser.add_argument("--prefix_output", help='The prefix of output file.', default='30')
    args = parser.parse_args()

    input_path_now = input_path.format(args.dataset, args.language, args.prefix_input)
    output_path_now = input_path.format(args.dataset, args.language, args.prefix_output)

    rows = read_tsv(input_path_now)

    # The first row is "INPUT:text"
    first_row = rows[0]
    rows = rows[1:]

    rows = np.random.choice(rows, args.length)

    with open(output_path_now, 'w', newline='\n') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow([first_row])

        for row in rows:
            writer.writerow([row])
