import json

class ResultRecord:
    def __init__(self, raw_data, pretty_print):
        self.data_dict = json.loads(raw_data)
        self.lang_code = self.data_dict['lang_code']
        self.category = self.data_dict['category']

        self.__pretty_print = pretty_print

    def __repr__(self):
        return self.__pretty_print.pformat(self.data_dict)
