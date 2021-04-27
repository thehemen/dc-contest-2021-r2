import csv
import pprint
import argparse

from data_record import DataRecord, get_full_text

input_path = '../../inputs-outputs/{}-{}-{}.txt'
output_path = '../../inputs-outputs/{}-{}-{}.tsv'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", help='The name of dataset.', default='dc0415-input')
    parser.add_argument("--language", help='The type of language (ar, en, fa, ru, uz).', default='en')
    parser.add_argument("--prefix", help='The prefix of output file.', default='1k')
    parser.add_argument("--max_recent_posts", type=int, help='The maximum number of recent posts.', default=3)
    parser.add_argument("--max_text_length", type=int, help='The maximum text length.', default=2000)
    parser.add_argument("--max_row_count", type=int, help='The maximum text row count.', default=25)
    args = parser.parse_args()

    input_path_now = input_path.format(args.dataset, args.language, args.prefix)
    output_path_now = output_path.format(args.dataset, args.language, args.prefix)

    pp = pprint.PrettyPrinter(indent=4)
    records = []

    with open(input_path_now, 'r') as f:
        for line in f.readlines():
            record = DataRecord(line, pp)
            text = get_full_text(record, args.max_recent_posts, args.max_text_length, args.max_row_count, is_clean=True)
            records.append(text)

    with open(output_path_now, 'w', newline='\n') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(['INPUT:text'])

        for record in records:
            writer.writerow([record])
