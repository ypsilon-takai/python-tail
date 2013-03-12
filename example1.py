#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:        tail sample
#
# Author:      Takai,Y (ypsilon.takai)
#
# Created:     06/03/2013
#-------------------------------------------------------------------------------

'''
Get every events from file.
'''

import tail

import time
import glob
import re


class WatchLog (object):

    def __init__(self):
        self.line_buffer = []
        self.finish = False
        self.callback = self.print_data

    def __del__(self):
        self.finish = True

    def regist_callback(self, f):
        self.callback = f

    def print_data (self, lines):
        for l in lines:
            print l

    def process_data (self, lines):
        self.callback(lines)

    def buffer_or_process (self, line):
        line = line.strip()
        if len(line) == 0 and len(self.line_buffer) != 0:
            self.process_data(self.line_buffer)
            self.line_buffer = []
        else:
            self.line_buffer.append(line)

    def create_tailer (self, targetfile, headortail):
        tailer = tail.Tail(targetfile, headortail, 2)
        tailer.register_callback(self.buffer_or_process)
        return tailer

    def get_newest_file (self, path):
        file_list = glob.glob(path)
        file_list.sort()
        return file_list.pop()

    def start(self):
        target_file = self.get_newest_file('D:/log/*')
        print "newfile : ", target_file
        tailer = self.create_tailer(target_file, 'tail')
        tailer.start()

        count = 100
        while count > 0:
            if self.finish:
                tailer.stop()
                tailer.join()
                break

            time.sleep(10)
            new_file = self.get_newest_file('D:/tmp/*')
            if new_file != target_file:
                print "New file has come!", new_file
                tailer.stop()
                tailer.join()
                print "Stopped. Create new."
                target_file = new_file
                tailer = self.create_tailer(target_file, 'head')
                tailer.start()

            count -= 1

        print 'end'

#================================================

def main():
    follower = WatchLog()
    follower.start()


if __name__ == '__main__':
    main()
