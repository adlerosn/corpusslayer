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
pluginName = os.path.abspath(__file__).split(os.path.sep)[-2]
pluginNameFriendly = (pluginName[0].upper()+pluginName[1:]).replace('_',' ')
from corpusslayer.hooks import getAnalysisOptionsEmptyContainer
from corpusslayer.bootstrap_constants import COLOR
from django.utils.translation import ugettext_lazy as _

def getAnalysisOptions():
    return []

def getExtraLangsMxpost():
    return {
        'id': 'pt-br-macmorpho',
        'lang': 'pt-br',
        'langfull': _('Portuguese (Brazil)'),
        'source': 'NILC/USP',
        'dir': os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'datasets',
            'mxpost'
        ),
    }

def getExtraLangsBrill():
    return {
        'id': 'pt-br-macmorpho',
        'lang': 'pt-br',
        'langfull': _('Portuguese (Brazil)'),
        'source': 'NILC/USP',
        'dir': os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'datasets',
            'brill'
        ),
    }

def getExtraLangsTreeTagger():
    return {
        'id': 'pt-br-macmorpho',
        'lang': 'pt-br',
        'langfull': _('Portuguese (Brazil)'),
        'source': 'NILC/USP',
        'dir': os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'datasets',
            'treetagger'
        ),
        'file': os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'datasets',
            'treetagger',
            'Trained80'
        ),
    }

def getHooks():
    return {
        'provider:brill:asset':[
            getExtraLangsBrill
        ],
        'provider:mxpost:asset':[
            getExtraLangsMxpost
        ],
        'provider:treetagger:asset':[
            getExtraLangsTreeTagger
        ],
    }