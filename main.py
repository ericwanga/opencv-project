# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import sys
import re
import os
import io
import configparser
import logging
import csv


class Utiliies(object):

    def __init__(self, configFile):
        self.__config = io.StringIO()
        self.__config.write('[dummysection]\n')
        self.__config.write(open(configFile).read())
        self.__cp = configparser.ConfigParser()

    def getFromConfig(self, param):
        self.__config.seek(0, os.SEEK_SET)
        self.__cp.read_file (self.__config)
        return str(self.__cp.get('dummysection', param))


class generateSql(object):
    def __init__(self):
        util = Utiliies('./config.txt')
        self.srcFilename = util.getFromConfig("fileName")
        self.transQ = util.getFromConfig("query_type_Transformation")

    def showParameters(self):
        print(self.srcFilename)
        print(self.transQ)



def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    generateSql().showParameters()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
