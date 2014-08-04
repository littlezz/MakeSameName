__author__ = 'zz'

import os
from os.path import isfile
from fnmatch import fnmatch
import re
import logging
logging.basicConfig(level=logging.WARNING, format='%(message)s',)


class Base:

    def __init__(self, extension, basedir='.'):
        self.extension = '.' + extension
        self.match = '*' + self.extension
        self.basedir = basedir
        self.files = []
        self.getfiles()
        self.orderfilse = OrdernumWithFiles(*self.files)
        logging.debug(self.orderfilse)

    def getfiles(self):
        self.files = [file for file in os.listdir('.') if isfile(file) and fnmatch(file, self.match)]


class OrdernumWithFiles(dict):

    def __init__(self, *args):
        """do not pass any things to dict"""

        super().__init__()
        self.flag = False
        self.order_analysis(*args)

    def order_analysis(self, *args):

        def getorder(tem, tem_list):

            for (seq_order, number) in enumerate(tem):
                other_same_col_item = [i[seq_order] for i in tem_list if i != tem]
                if number not in other_same_col_item:
                    return number

        pat = re.compile(r'\d+')
        tem_list = []
        for filename in args:
            tem_list.append(re.findall(pat, filename))

        for filename in args:
            tem = re.findall(pat, filename)
            order = getorder(tem, tem_list)
            self.__setitem__(order, filename)

    def __setitem__(self, key, val):
        self.__rename(key, val)
        super().__setitem__(key, val)

    def __rename(self, key, val):
        if self.flag:
            try:
                logging.debug('rename: %s to %s', self[key], val)
                os.rename(self[key], val)
            except KeyError:
                print('no %s sub!' % key)

    def rename_avaliable(self):
        self.flag = True


def main():


    print('now dir is %s' % os.getcwd())
    video_key = input('video file extension (for example, mp4) ')
    video_file = Base(video_key)
    sub_key = input('sub file extension (for example ass)')
    sub_file = Base(sub_key)
    sub_file.orderfilse.rename_avaliable()

    for key, val in video_file.orderfilse.items():
        sub_file.orderfilse[key] = val.rstrip(video_file.extension) + sub_file.extension

if __name__ == '__main__':
    main()