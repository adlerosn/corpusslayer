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

randfactor = 0.2658954

def getAnalysisOptions():
    nuketagged = getAnalysisOptionsEmptyContainer(
        pluginName = pluginName,
    )
    nuketagged['text'] = _('Delete processed data [TreeTagger]')
    nuketagged['priority'] = -2000+randfactor
    nuketagged['icon'] = 'close'
    nuketagged['link'] = pluginName+'_nuke'
    nuketagged['color'] = COLOR.RED
    createtagged = getAnalysisOptionsEmptyContainer(
        pluginName = pluginName,
    )
    createtagged['text'] = _('Process Corpus [TreeTagger]')
    createtagged['priority'] = -1000+randfactor
    createtagged['icon'] = 'arrow-right'
    createtagged['link'] = pluginName+'_process'
    createtagged['color'] = COLOR.GREEN
    tagged = getAnalysisOptionsEmptyContainer(
        pluginName = pluginName,
    )
    tagged['text'] = _('Tagged Text [TreeTagger]')
    tagged['icon'] = 'tags'
    tagged['priority'] = 195+randfactor
    return [
        nuketagged,
        createtagged,
        tagged,
    ]

import json
from django.urls import reverse
from django.http import HttpResponseRedirect
importline1 = 'import '+('.'.join(['plugins',pluginName,'models'])+' as models')
exec(importline1) #import plugins.thisplugin.models as models

def getSentenceTagged(corpus):
    val = None
    try:
        val = json.loads(models.CorpusTreetagged.objects.get(corpus__pk=corpus.pk).postags)
    except:
        val = HttpResponseRedirect(reverse(pluginName+'_process',None,[corpus.pk]))
    return {
        'key': pluginName,
        'name': 'TreeTagger',
        'sentences': val,
    }

def getHooks():
    return {
        'query:sentencetokenstagged':[
            getSentenceTagged
        ],
    }
