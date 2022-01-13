import json
import time
from datetime import datetime
from json import JSONDecoder, JSONEncoder, JSONDecodeError
import logging
# from main.log import *
import mysql.connector as mysql
from mysql.connector import Error
import pathlib as pl

logTime = datetime.now().strftime("%Y_%m_%d.%H_%M_%S")

italic = '\33[3m'
# bold = '\33[1m'
bold = ''
reset = '\033[0m'
yellow = '\33[33m'
red = '\33[31m'
green = '\033[92m'
blue = '\033[94m'
violet = '\33[35m'
cyan = '\u001b[36m'
white = '\u001b[37m'
tick = bold + green + "\u2713" + reset + blue
x = bold + red + 'x' + reset + blue


class logger(object):

    @staticmethod
    def formatter(logState, logData):
        print(
            bold + f"{red + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + reset} - {bold + logState + reset} - "
                   f"{bold + green + logData}" + reset)

    @classmethod
    def log(cls, logData):
        return cls.formatter(blue + 'LOG', logData)

    @classmethod
    def warn(cls, logData):
        return cls.formatter(red + 'WARNING', logData)

    @classmethod
    def err(cls, logData):
        return cls.formatter(red + 'ERROR', red + logData + reset)

    @classmethod
    def info(cls, logData):
        return cls.formatter(cyan + 'INFO' + reset, logData)

    @classmethod
    def fail(cls, logData):
        return cls.formatter(red + 'FAILED', red + logData + reset)

    @staticmethod
    def subLog(data):
        print('\t', bold + blue + data + reset)

    @staticmethod
    def subLog_(data):
        print(bold + blue + data + reset)


logger_c = logging.getLogger('schemaDiff')
logger_c.setLevel(logging.DEBUG)
log_format = logging.Formatter(f'%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)
consoleHandler.setFormatter(log_format)
logger_c.addHandler(consoleHandler)

logger_c.info('Schemadiff Database Evaluator Command Line Interface (version 2.0)')
logger_c.debug('Loading ec2 keys for database servers')

time.sleep(0.1)

with open('config.json', 'r') as config_params:
    config_ = config_params.read()
    load_config = json.loads(config_)

logger.subLog_('---------< - Available Servers - >---------')
__key_length = len(load_config['ec2_keys'])
for __id in range(0, __key_length):
    for __server in load_config["ec2_keys"][__id]:
        print(__server, '-', load_config["ec2_keys"][__id][__server])
        # logger.subLog_(f"{__server} - {load_config['ec2_keys'][__id][__server]}")

schema_config = {
    "host": "10.95.60.192",
    "user": "schemaAdmin",
    "password": "YfYv&t[Sas>N9pyH",
    "port": "3306",
    "database": "information_schema",
    "auth_plugin": "mysql_native_password"
}


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
        """
        Check for directories required for the tool, the paths about directories are inherited from config.json.
        If a directory is missing in the system a new directory is created, this is essential for file operations
        in schemadiff tool to export and compare raw schema files.
        """
        try:
            logger.subLog_('--------< - Directory Checklist - >--------')
            for _id in range(0, self.key_length_):
                for _dir in self.working_dirs_[_id]:
                    if pl.Path(self.working_dirs_[_id][_dir]).exists():
                        print(_dir, '->', 'directory exists')
                    else:
                        print(_dir, '->', 'does not exists, creating directory at the moment.')
                        pl.Path(self.working_dirs_[_id][_dir]).mkdir()
        except NotADirectoryError as nae:
            logger_c.error('Found error while checking working directories')


class mysql_connect(properties, config_decoder):

    def __init__(self, ):
        super().__init__()
        self._config = schema_config
        self._connect = None
        self._name = None
        self._database_schemas = []
        self._table_names = []
        self._ttl_schemas = 0

    def get_cursor(self):
        try:
            self._connect = mysql.connect(**self._config, connect_timeout=5)
            if self._connect.is_connected():
                # logger.debug(f'Connection established successfully with {self.name} database.')
                return self._connect.cursor()
        except Error as mysql_connect_err:
            logger_c.error(f'Found error while connecting to {self._name} database.')

    def extract_metadata(self):

        try:
            logger.subLog_('---------< - Exportable Schemas - >--------')
            fetch_dbs = "select distinct(TABLE_SCHEMA), count(TABLE_NAME) Tables from information_schema.TABLES " \
                        "where TABLE_SCHEMA not in ('mysql','information_schema','sys','performance_schema') group by " \
                        "TABLE_SCHEMA;"
            cursor = self.get_cursor()
            cursor.execute(fetch_dbs)
            a = cursor.fetchall()
            # print(tabulate.tabulate(a, tablefmt='fancy_grid', headers=['Database_Name', 'Tables']))
            for database in a:
                self._database_schemas.append(database[0])
                self._table_names.append(database[1])
                print(f'{database[0]} -> {database[1]}')
        except Error as mysql_tbl_err:
            logger_c.error(f'Found error while populating tables.')

        for _count in range(0, len(self._table_names)):
            self._ttl_schemas = self._ttl_schemas + self._table_names[_count]
        logger.subLog_(f'{green}Total number of schemas to export : {self._ttl_schemas}')




if __name__ == '__main__':
    db_ops = mysql_connect()
    db_ops.check_directories()
    db_ops.extract_metadata()
    db_ops.__str__()
