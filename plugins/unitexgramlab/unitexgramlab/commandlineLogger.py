#!/usr/bin/env python3
#  -*- encoding: utf-8 -*-

# Copyright (c) 2017 Adler Neves <adlerosn@gmail.com>
#
# MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

__author__ = "Adler Neves"
__email__ = "adlerosn@gmail.com"
__title__ = None
__description__ = None
__license__ = 'MIT'
__copyright__ = 'Copyright 2017 Adler O. S. Neves'
__version__ = '0.0.1'

import os
import json

pluginName = os.path.abspath(__file__).split(os.path.sep)[-3]
exec('from '+('.'.join(['plugins',pluginName,'unitexgramlab','objectify']))+' import Objectify')

def check_pid(pid):
    try:
        os.kill(pid, 0) # inofensivo ao processo que recebe
    except OSError:
        return False
    else:
        return True

class TaskLogger(object):
    folder = ''
    beganFile = ''
    completedFile = ''
    erroredFile = ''
    _title = ''
    def __init__(self, folder, title, began = False, completed = False):
        self.folder = folder
        self._title = title
        fsep = self.folder+os.path.sep
        self.beganFile = fsep+"began.flag"
        self.completedFile = fsep+"completed.flag"
        self.erroredFile = fsep+"errored.flag"
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
        if began:
            self.began = True
        if completed:
            self.completed = True

    @property
    def title(self):
        return self._title

    @property
    def began(self):
        return os.path.isfile(self.beganFile)

    @began.setter
    def began(self, res):
        if res:
            with open(self.beganFile, 'a+'):
                os.utime(self.beganFile, None)
        elif self.began:
            os.remove(self.beganFile)

    @property
    def completed(self):
        return os.path.isfile(self.completedFile)

    @completed.setter
    def completed(self, res):
        if res:
            self.began = True
            with open(self.completedFile, 'a+'):
                os.utime(self.completedFile, None)
        elif self.completed:
            os.remove(self.completedFile)

    @property
    def errored(self):
        return os.path.isfile(self.erroredFile)

    @errored.setter
    def errored(self, res):
        if res:
            self.began = True
            with open(self.erroredFile, 'a+'):
                os.utime(self.erroredFile, None)
        elif self.errored:
            os.remove(self.erroredFile)

    @property
    def result(self):
        r = dict()
        fsep = self.folder+os.path.sep
        try:
            with open(fsep+"commandArgv.json", 'r') as f:
                r['args'] = json.loads(f.read())
            with open(fsep+"returncode.txt", 'r') as f:
                r['returncode'] = int(f.read())
            with open(fsep+"stdout.bin",'rb') as f:
                r['stdout'] = f.read()
            with open(fsep+"stdout.txt",'rt') as f:
                r['stdoutText'] = f.read()
            with open(fsep+"stderr.bin",'rb') as f:
                r['stderr'] = f.read()
            with open(fsep+"stderr.txt",'rt') as f:
                r['stderrText'] = f.read()
        except FileNotFoundError:
            return None
        return Objectify(r)

    @result.setter
    def result(self, res):
        self.began = True
        fsep = self.folder+os.path.sep
        with open(fsep+"commandArgv.json", 'w') as f:
            f.write(json.dumps(res.args))
        with open(fsep+"returncode.txt",'wt') as f:
            f.write(str(int(res.returncode)))
            if int(res.returncode) != 0:
                self.errored = True
        with open(fsep+"stdout.bin",'wb') as f:
            dt = bytes()
            if res.stdout is not None:
                dt = res.stdout
            f.write(dt)
        with open(fsep+"stdout.txt",'wt') as f:
            dt = ''
            if res.stdout is not None:
                dt = (
                    res.stdout.
                    decode('utf-8', errors='replace').
                    replace('\r\r','\r').
                    replace('\r\n','\n').
                    replace('\r','\n')
                )
            f.write(dt)
        with open(fsep+"stderr.bin",'wb') as f:
            dt = bytes()
            if res.stderr is not None:
                dt = res.stderr
            f.write(dt)
        with open(fsep+"stderr.txt",'wt') as f:
            dt = ''
            if res.stderr is not None:
                dt = (
                    res.stderr.
                    decode('utf-8', errors='replace').
                    replace('\r\r','\r').
                    replace('\r\n','\n').
                    replace('\r','\n')
                )
            f.write(dt)
        self.completed = True

    @property
    def _jsonable(self):
        simple = dict()
        simple['title'] = self.title
        simple['began'] = self.began
        simple['completed'] = self.completed
        simple['errored'] = self.errored
        simple['result'] = self.result
        if simple['result'] is not None:
            simple['result'] = simple['result'].as_dict
            simple['result']['stdout'] = simple['result']['stdout'].decode('utf-8', errors='ignore')
            simple['result']['stderr'] = simple['result']['stderr'].decode('utf-8', errors='ignore')
        return simple

    def __repr__(self):
        return json.dumps(self._jsonable)

    def __str__(self):
        return self.folder

class CommandLogger(object):

    _folder = ''
    _length = 0

    def __init__(self, folder="logs", dontTouchPid = False):
        self._folder = folder
        if not os.path.exists(self._folder):
            os.makedirs(self._folder)
        self._updateLength()
        if not dontTouchPid:
            self.__pid = os.getpid()

    @property
    def _expectedLength(self):
        try:
            with open(os.path.abspath(self._folder+os.path.sep+'plannedSize')+".txt") as f:
                rd = f.read()
                if rd:
                    return int(rd)
                else:
                    return 0
        except:
            return 0

    @_expectedLength.setter
    def _expectedLength(self, newValue):
        with open(os.path.abspath(self._folder+os.path.sep+'plannedSize')+".txt", 'w') as f:
            f.write(str(newValue))

    def _updateLength(self,fromBeginning=False):
        if fromBeginning:
            self._length = 0
        while os.path.exists(self._nextEntry):
            self._length+=1
        if self._expectedLength < self._length:
            self._expectedLength = self._length

    @property
    def _nextEntry(self):
        return self._getEntry(self._length+1)

    def _getEntry(self, num):
        return self._folder+os.path.sep+str(num)

    def task(self, title="", began=False, completed=False):
        self.__pid = os.getpid()
        self._updateLength()
        with open(self._nextEntry+".txt", 'w') as f:
            f.write(title)
        tl = TaskLogger(self._nextEntry, title, began, completed)
        self._updateLength()
        return tl

    def _reopenTask(self, num):
        title = ''
        with open(self._getEntry(num)+".txt") as f:
            title = f.read()
        return TaskLogger(self._getEntry(num), title)

    @property
    def done(self):
        try:
            with open(os.path.abspath(self._folder+os.path.sep+'done')+".txt") as f:
                return str(True) == f.read()
        except:
            return False

    @done.setter
    def done(self, newValue):
        with open(os.path.abspath(self._folder+os.path.sep+'done')+".txt", 'w') as f:
            f.write(str(newValue))

    @property
    def __pid(self):
        try:
            with open(self._folder+os.path.sep+".pid") as f:
                return int(f.read())
        except FileNotFoundError:
            return os.getpid()
    @__pid.setter
    def __pid(self, pid):
        with open(self._folder+os.path.sep+".pid", 'w') as f:
            f.write(str(pid))

    @property
    def _running(self):
        return check_pid(self.__pid)

    @property
    def aborted(self):
        return not self._running and not self.done

    @property
    def tasks(self):
        return [self._reopenTask(i+1) for i in range(self._length)]

    def planTasks(self,num):
        self._updateLength()
        self._expectedLength+=num
        self._updateLength()

    @property
    def summary(self):
        d = dict()
        a = self.tasks
        b = [x.began for x in a]
        c = [x.completed for x in a]
        e = [x.errored for x in a]
        d['expected_length'] = self._expectedLength
        d['current_length'] = self._length
        d['done'] = self.done
        d['aborted'] = self.aborted
        d['allbegan'] = all(b)
        d['allcompleted'] = all(c)
        d['anyerrored'] = any(e)
        return d

    @property
    def _jsonable(self):
        s = self.summary
        s.update([('tasks',list(map(lambda a: a._jsonable, self.tasks)))])
        return s

    def __repr__(self):
        return json.dumps(self._jsonable)

    def __str__(self):
        return self._folder
