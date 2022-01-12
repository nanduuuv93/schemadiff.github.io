from datetime import datetime
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



"""
key_length = len(load_config['ec2_keys'])
            for _id in range(0, key_length):
                for _server in load_config["ec2_keys"][_id]:
                    print(_server,
                          load_config["ec2_keys"][_id][_server])

"""