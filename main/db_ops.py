import json
import time
from json import JSONDecoder, JSONEncoder, JSONDecodeError
import logging
from main.log import *
from rich import print
from rich.console import Console
import mysql.connector as mysql
from mysql.connector import errorcode, Error, DatabaseError, DataError
import tabulate

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

with open('../main/config.json', 'r') as config_params:
    config_ = config_params.read()
    load_config = json.loads(config_)

logger.subLog_('---------< - Available Servers - >---------')
__key_length = len(load_config['ec2_keys'])
for __id in range(0, __key_length):
    for __server in load_config["ec2_keys"][__id]:
        print(__server, '-', load_config["ec2_keys"][__id][__server])
        # logger.subLog_(f"{__server} - {load_config['ec2_keys'][__id][__server]}")

schema_config = {'host': 'localhost', 'port': '3306', 'user': 'schemaUser', 'password': 'schemaUser@@1',
                 'database': 'information_schema'}


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


class schemadiff(properties, config_decoder):

    def __init__(self, ):
        super().__init__()
        self._config = schema_config
        self._connect = None
        self._name = None
        self._database_schemas = []
        self._table_names = []
        self._ttl_schemas = 0

    def get_cursor(self):
        """
        Creates reusable cursor, if the db params are valid.
        :return: created cursor
        """
        try:
            self._connect = mysql.connect(**self._config, connect_timeout=5)
            if self._connect.is_connected():
                # logger.debug(f'Connection established successfully with {self.name} database.')
                return self._connect.cursor()
        except Error as mysql_connect_err:
            logger_c.error(f'Found error while connecting to {self._name} database.')
            if mysql_connect_err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                logger_c.error('Access denied to user ! Please check the database parameter passed in config file.')

    def extract_metadata(self):
        """
        Extract database and table metadata from information_schema repository, this data is later used to
        compute, extract schema and apply changes.
        :return: database_schema, tables
        """
        try:
            logger.subLog_('---------< - Exportable Schemas - >--------')
            fetch_dbs = "select distinct(TABLE_SCHEMA), count(TABLE_NAME) Tables from " \
                        "information_schema.TABLES " \
                        "where TABLE_SCHEMA not in ('mysql','information_schema','sys','performance_schema') group by " \
                        "TABLE_SCHEMA"
            cursor = self.get_cursor()
            cursor.execute(fetch_dbs)
            a = cursor.fetchall()
            print(tabulate.tabulate(a,
                                    tablefmt='fancy_grid',
                                    stralign="center",
                                    numalign="center",
                                    headers=['Schema', 'Tables', 'Engine']))
            for database in a:
                self._database_schemas.append(database[0])
                self._table_names.append(database[1])
                # print(f'{database[0]} -> {database[1]}')
        except Error as mysql_tbl_err:
            logger_c.error(f'Found error while populating tables.')

    def __str__(self):
        if len(self._table_names) != 0:
            for _count in range(0, len(self._table_names)):
                self._ttl_schemas = self._ttl_schemas + self._table_names[_count]
            logger.subLog_(f'{green}Total number of schemas to export : {self._ttl_schemas}')
        else:
            logger.debug('There are no tables to compare.')

    @classmethod
    def run(cls):
        db_ops = schemadiff()
        db_ops.check_directories()
        db_ops.extract_metadata()
        db_ops.__str__()


if __name__ == '__main__':
    schemadiff.run()
