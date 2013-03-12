#-------------------------------------------------------------------------------
# Name:        tail
# Purpose:     Tail -f specified file in anther thread.
#
# Author:      Takai,Y (ypsilon.takai)
#
# Created:     06/03/2013
#-------------------------------------------------------------------------------
'''
Tail tool -- Unix 'tail -f' like functionality in python.

Work as another thread for asyncronous file watching.

Usage:
1. Create with args.
  tailed_file : <file path>
     Target file to tail -f.
  headortail  : (head|tail)
     File contents will be output from top-most position if 'head' is specified.
     Else, read point will move to bottom and only new contents will be output.
  interval    : <sec>
     Checks new entry every interval seconds.
2. Set callback func with register_callback.
  func  : <call back func>
     Func will be called with single line text. If multiple lines will come, 
     func will be called multiple times for every lines.

3. Call start to start.

'''

import os
import sys
import time
import threading

class Tail(threading.Thread):

    def __init__(self, tailed_file, headortail='head', interval=5):
        self.check_file_validity(tailed_file)

        threading.Thread.__init__(self)

        self.tailed_file = tailed_file
        self.callback = sys.stdout.write
        self.headortail = headortail
        self.finish = False
        self.interval = interval

    def __del__ (self):
        self.finish = True

    def run(self):
        self.follow()

    def stop (self):
        self.finish = True

    def follow(self):
        with open(self.tailed_file) as file_:
            # Go to the end of file
            if self.headortail == 'tail':
                file_.seek(0,2)
            else:
                file_.seek(0,0)

            while True:
                curr_position = file_.tell()
                line = file_.readline()
                if not line:
                    file_.seek(curr_position)
                    time.sleep(self.interval)
                else:
                    self.callback(line)

                if self.finish:
                    break

    def register_callback(self, func):
        ''' Overrides default callback function to provided function. '''
        self.callback = func

    def set_intarval (self, interval):
        self.interval = interval


    def check_file_validity(self, file_):
        ''' Check whether the a given file exists, readable and is a file '''
        if not os.access(file_, os.F_OK):
            raise TailError("File '%s' does not exist" % (file_))
        if not os.access(file_, os.R_OK):
            raise TailError("File '%s' not readable" % (file_))
        if os.path.isdir(file_):
            raise TailError("File '%s' is a directory" % (file_))

class TailError(Exception):
    def __init__(self, msg):
        self.message = msg
    def __str__(self):
        return self.message
