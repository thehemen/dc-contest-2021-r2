import re
import json
import string

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
        text = self.title + '\n'

        if len(self.description) > 0:
            text += self.description + '\n'

        for recent_post in self.recent_posts:
            if len(recent_post) > 0:
                text += recent_post + '\n'

        return text

    def __repr__(self):
        return self.__pretty_print.pformat(self.data_dict)
