import json

class DataRecord:
    def __init__(self, raw_data, pretty_print):
        self.data_dict = json.loads(raw_data)
        self.title = self.data_dict['title']
        self.description = self.data_dict['description']
        self.recent_posts = [x['text'] for x in self.data_dict['recent_posts']]
        self.full_text = self.__get_full_text(self.title, self.description, self.recent_posts)

        self.lang_code = 'other'
        self.__pretty_print = pretty_print

    def __hash__(self):
        return hash(self.__str__())

    def __str__(self):
        return self.full_text

    def __repr__(self):
        return self.__pretty_print.pformat(self.data_dict)

    def __get_full_text(self, title, description, recent_posts):
        text = title[:] + '\n'
        text += description + '\n'

        for post in self.recent_posts:
            text += post + '\n'

        return text
