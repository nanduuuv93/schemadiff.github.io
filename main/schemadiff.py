import json
import time
from json import JSONDecoder, JSONEncoder, JSONDecodeError
import logging
from main.log import *
from rich import print
from rich.console import Console

logger_c = logging.getLogger('schemaDiff')
logger_c.setLevel(logging.DEBUG)
log_format = logging.Formatter(f'%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)
consoleHandler.setFormatter(log_format)
logger_c.addHandler(consoleHandler)

logger_c.info('Schemadiff Database Evaluator Command Line Interface')
logger_c.debug('Loading ec2 keys for database servers')

time.sleep(0.1)

with open('../main/config.json', 'r') as config_params:
    config_ = config_params.read()
    load_config = json.loads(config_)

logger.subLog_('Available Servers')
__key_length = len(load_config['ec2_keys'])
for __id in range(0, __key_length):
    for __server in load_config["ec2_keys"][__id]:
        print(__server, '-', load_config["ec2_keys"][__id][__server])

"""
logger.subLog_('Working Directories')
___key_length = len(load_config['working_directories'])
for ___id in range(0, ___key_length):
    for ___dir in load_config["working_directories"][___id]:
        print(___dir, '->', load_config["working_directories"][___id][___dir])
"""


class config_decoder(object):

    def __init__(self, key_length=None, key=None, value=None):
        self._length = key_length
        self.key_ = key
        self._value = value

    def get_ec2Keys(self, key_v):
        """
        Get ec2 keys from config.
        :param key_v:
        :return: ec2 value
        """
        try:
            self._length = len(load_config['ec2_keys'])
            for _id in range(0, self._length):
                for _server in load_config["ec2_keys"][_id]:
                    if _server == key_v:
                        logger_c.debug(load_config["ec2_keys"][_id].get(_server))
        except JSONDecodeError as jde:
            logger_c.error('Found error while accessing ec2 connectable keys from config.')

    @classmethod
    def get_ec2keys(cls, key):
        """
        Get ec2 keys from config
        :param key:
        :return: key_value
        """
        try:
            key_length = len(load_config['ec2_keys'])
            for _id in range(0, key_length):
                for _server in load_config["ec2_keys"][_id]:
                    if _server == key:
                        logger_c.info(load_config["ec2_keys"][_id].get(_server))
        except JSONDecodeError as jde:
            logger_c.error('Found error while accessing ec2 connectable keys from config.')

    @classmethod
    def get_wDirs(cls, key):
        """
        Get working directories
        :return:
        """
        try:
            key_length = len(load_config['working_directories'])
            for _id in range(0, key_length):
                for _dir in load_config["working_directories"][_id]:
                    if _dir == key:
                        return load_config["working_directories"][_id].get(_dir)
        except JSONDecodeError as jde:
            logger_c.error('Found error while accessing working directories config.')


class properties(config_decoder):

    def __init__(self):
        super().__init__()
        self.working_dirs_ = []
        self.key_length_ = len(load_config['working_directories'])
        for _id_ in range(0, self.key_length_):
            for _dir_ in load_config["working_directories"][_id_]:
                self.working_dirs_.append({_dir_: load_config["working_directories"][_id_][_dir_]})

    def check_directories(self):
        try:
            logger.subLog_('Directory Checklist')
            for _id in range(0, self.key_length_):
                for _dir in self.working_dirs_[_id]:
                    if pl.Path(self.working_dirs_[_id][_dir]).exists():
                        print(_dir, '->', 'exists')
                    else:
                        print(_dir, '->', 'does not exists, creating directory at the moment.')
                        pl.Path(self.working_dirs_[_id][_dir]).mkdir()
        except NotADirectoryError as nae:
            logger_c.error('Found error while checking working directories')


if __name__ == '__main__':
    props = properties()
    props.check_directories()
