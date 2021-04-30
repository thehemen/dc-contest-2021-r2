import os
import tqdm
import argparse

dc_types = ['dc0415-input', 'dc0421-input', 'dc0428-input']
dc_texts = ['original', 'translated']
dc_langs = ['all', 'ar', 'en', 'fa', 'ru', 'uz']

dc_concat = 'dc-concat'
input_path = '../../inputs/{0}/{1}/{0}-{2}{3}.txt'

if __name__ == '__main__':
    with tqdm.tqdm(total=len(dc_types) * len(dc_texts) * len(dc_langs)) as tqdm_bar:
        for dc_text in dc_texts:
            translation_prefix = '-translated' if dc_text == 'translated' else ''

            for dc_lang in dc_langs:
                content = ''

                for dc_type in dc_types:
                    input_path_now = input_path.format(dc_type, dc_text, dc_lang, translation_prefix)

                    with open(input_path_now, 'r') as f:
                        content += f.read()

                    tqdm_bar.update(1)

                output_path_now = input_path.format(dc_concat, dc_text, dc_lang, translation_prefix)

                with open(output_path_now, 'w') as f:
                    f.write(content)
