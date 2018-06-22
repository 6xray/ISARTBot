# -*- coding: utf-8 -*-

"""
MIT License

Copyright (c) 2018 Renondedju

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from datetime import datetime

class Logs():
    """
    Used to log any activity
    """

    def __init__(self, dir: str = "./logs.log", enabled: bool = True):

        #Public
        self.enabled = enabled

        #Private
        self.__logs_file = None

        #Setup
        try:
            self.__logs_file = open(dir, "a")
        except:
            self.__logs_file = None
            print("Warning : no logs file found !")

    def print(self, *args):
        """
        Logs every args into the console and
        the file (if the opening is successful)
        """

        #Generating the output
        str_args = []
        for i in range(len(args)):
            str_args.append(str(args[i]))

        output = " "
        output = output.join(args)
        date   = datetime.now().strftime('%Y/%m/%d at %H:%M:%S')
        output = date + " - " + output

        print(output)
        if (self.__logs_file != None and self.__logs_file.writable()):
            self.__logs_file.write(output + '\n')

        return

    def __del__(self):

        if (self.__logs_file != None):
            self.__logs_file.close()