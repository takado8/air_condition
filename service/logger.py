import json
import os
from datetime import datetime

LOG_FILE_PATH = '../log/log.json'


class Logger:
    def __init__(self):
        if not os.path.isdir(os.path.dirname(LOG_FILE_PATH)):
            os.mkdir(os.path.dirname(LOG_FILE_PATH))
        if not os.path.isfile(LOG_FILE_PATH):
            with open(LOG_FILE_PATH, 'x'):
                pass

    def append_record(self, record_dict):
        record_dict['date'] = self.get_datetime()
        with open(LOG_FILE_PATH, 'a') as f:
            json.dump(record_dict, f)
            f.write('\n')

    def load_log(self):
        with open(LOG_FILE_PATH) as f:
            my_list = [json.loads(line) for line in f]
        return my_list

    def get_datetime(self):
        now = datetime.now()
        return now.strftime("%d.%m.%Y %H:%M:%S")


if __name__ == '__main__':
    logger = Logger()
    logger.load_log()