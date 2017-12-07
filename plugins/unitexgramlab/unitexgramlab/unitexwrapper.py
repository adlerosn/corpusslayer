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
__title__ = 'unitexwrapper'
__description__ = 'A wrapper for Unitex/GramLab which uses the commandline'
__license__ = 'MIT'
__copyright__ = 'Copyright 2017 Adler Neves'
__version__ = '0.0.1'

import os
import subprocess

operatingSystem = os.name

if operatingSystem == 'java':
    import java.lang.System
    osBelowJvm = java.lang.System.getProperty('os.name').lower()
    if 'ce' in osBelowJvm:
        operatingSystem = 'ce'
    elif 'win' in osBelowJvm:
        operatingSystem = 'nt'
    elif 'mac' in osBelowJvm:
        operatingSystem = 'posix'
    elif any([unixPart in osBelowJvm for unixPart in ['ix','ux','bsd']]):
        operatingSystem = 'posix'
    elif any([solarisPart in osBelowJvm for solarisPart in ['sun os','sunos','solaris']]):
        operatingSystem = 'os2'
    elif 'riscos' in osBelowJvm:
        operatingSystem = 'riscos'
    else:
        operatingSystem = 'java over unknown: '+osBelowJvm

if operatingSystem not in ['posix', 'nt']:
    raise ImportError("This module can't be imported on this platform: \"%s\""%operatingSystem)

unitex_default = './UnitexToolLogger' if operatingSystem == 'posix' else 'UnitexToolLogger.exe'

class Unitex:
    def __init__(self, unitex_path = unitex_default):
        self.unitex_path = unitex_path
    def __getattr__(self, utility):
        return UnitexUtility(self.unitex_path, utility)

class UnitexUtility:
    def __init__(self, path, utility):
        self.path = path
        self.utility = utility
    def __call__(self, *args):
        return subprocess.run(
            [self.path, self.utility] + list(args),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
