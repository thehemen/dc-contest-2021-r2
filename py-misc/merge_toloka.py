import csv
import argparse

input_path = '../../inputs-outputs/{}-{}-{}.tsv'
output_path = '../../inputs-outputs/{}-{}-{}-{}.tsv'

def read_tsv(path):
    lines = []

    with open(path, 'r', newline='\n') as f:
        reader = csv.reader(f, delimiter='\t')

        for line in reader:
            lines.append(line[0])

    return lines

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_first", help='The name of the first dataset.', default='dc0415-input')
    parser.add_argument("--dataset_second", help='The name of the first dataset.', default='dc0421-input')
    parser.add_argument("--language", help='The type of language (ar, en, fa, ru, uz).', default='en')
    parser.add_argument("--prefix_input", help='The prefix of input file.', default='1k')
    parser.add_argument("--prefix_output", help='The prefix of output file.', default='2k')
    args = parser.parse_args()

    input_path_first = input_path.format(args.dataset_first, args.language, args.prefix_input)
    input_path_second = input_path.format(args.dataset_second, args.language, args.prefix_input)
    output_path_merged = output_path.format(args.dataset_first.split('-')[0], args.dataset_second,
        args.language, args.prefix_output)

    rows = []
    rows.extend(read_tsv(input_path_first))
    rows.extend(read_tsv(input_path_second)[1:])

    with open(output_path_merged, 'w', newline='\n') as f:
        writer = csv.writer(f, delimiter='\t')

        for row in rows:
            writer.writerow([row])
