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

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRETS_DIR = os.path.join(BASE_DIR,'secrets')

SKB = os.path.join(SECRETS_DIR,'SECRET_KEY.bin')
DBG = os.path.join(SECRETS_DIR,'DEBUG.txt')
STD = os.path.join(SECRETS_DIR,'SITE.tld')
STN = os.path.join(SECRETS_DIR,'SITE.txt')
MAILCFG = os.path.join(SECRETS_DIR,'mailconfig.py')
RGO = os.path.join(SECRETS_DIR,'REGISTRATION_OPEN.txt')
LNGS = os.path.join(BASE_DIR,'locale')
LNGSo = os.path.join(SECRETS_DIR,'active_languages.html')

if not os.path.exists(SECRETS_DIR):
    os.makedirs(SECRETS_DIR)

if not os.path.exists(LNGS):
    os.makedirs(LNGS)

if not os.path.exists(SKB):
    with open(SKB,'wb') as f:
        f.write(os.urandom(512))

if not os.path.exists(MAILCFG):
    with open(MAILCFG,'wt') as f:
        f.write('\n')

if not os.path.exists(DBG):
    with open(DBG,'wt') as f:
        f.write('False')

if not os.path.exists(RGO):
    with open(RGO,'wt') as f:
        f.write('True')

if not os.path.exists(STD):
    with open(STD,'wt') as f:
        f.write('the.corpusslayer.com')

if not os.path.exists(STN):
    with open(STN,'wt') as f:
        f.write('Corpus Slayer')

def isTrue(s: str) -> bool:
    return s in ['1','true','t','True','TRUE','yes','y','YES','Yes']

SECRET_KEY = None
DEBUG = None
SITE_DOMAIN = None
REGISTRATION_OPEN = None
SITE_NAME = None
LANGUAGES = list()

with open(SKB,'rb') as f:
    SECRET_KEY = f.read()

with open(DBG,'rt') as f:
    DEBUG = isTrue(f.read().strip())

with open(RGO,'rt') as f:
    REGISTRATION_OPEN = isTrue(f.read().strip())

with open(STD,'rt') as f:
    SITE_DOMAIN = f.read().strip()

with open(STN,'rt') as f:
    SITE_NAME = f.read().strip()

for language_code in sorted(os.listdir(LNGS)):
    lc = language_code.lower().replace(' ','-').replace('_','-')
    LANGUAGES.append((
        lc,
        'lang__'+lc
    ))

with open(LNGSo,'wt') as f:
    f.write('{# Autogenerated document for the sole purpose of triggering ')
    f.write('addition of translation entry in internationalization framework #}\n')
    f.write('<ol>\n\t')
    f.write('\n\t'.join([
        '<li id="%s">{%% trans \'%s\' %%}</li>'%(
            lang_code,
            lang_trans.replace('\\','\\\\').replace('\'','\\\''),
        )
        for lang_code, lang_trans in LANGUAGES
    ]))
    f.write('\n</ol>\n')
