import re
import json
import string

puncs = set(string.punctuation)
puncs.update([' ', '\n'])

def clean(text):
    text = re.sub(' +', ' ', text.replace('\t', ' '))
    return ''.join(x for x in text if x.isdigit() or x.isalpha() or x in puncs)

def get_full_text(dataRecord, max_recent_posts=None, max_text_length=None, max_row_count=None, is_clean=False):
    title = clean(dataRecord.title) if is_clean else dataRecord.title
    description = clean(dataRecord.description) if is_clean else dataRecord.description

    text = title + '\n\n'

    if len(description) > 0:
        text += description + '\n\n'

    recent_posts = dataRecord.recent_posts

    if max_recent_posts is not None:
        recent_posts = recent_posts[:max_recent_posts]

    for i, recent_post in enumerate(recent_posts):
        recent_post = clean(recent_post) if is_clean else recent_post

        if len(recent_post) > 0:
            text += recent_post + '\n\n'

    if max_text_length is not None:
        text = text[:max_text_length]

    if max_row_count is not None:
        text = '\n'.join(row for row in text.split('\n')[:max_row_count])

    return text

class DataRecord:
    def __init__(self, raw_data, pretty_print):
        self.data_dict = json.loads(raw_data)
        self.title = self.data_dict['title']
        self.description = self.data_dict['description']
        self.recent_posts = [x['text'] for x in self.data_dict['recent_posts']]

        self.lang_code = 'other'
        self.__pretty_print = pretty_print

    def __hash__(self):
        return hash(self.__str__())

    def __str__(self):
        return get_full_text(self)

    def __repr__(self):
        return self.__pretty_print.pformat(self.data_dict)
