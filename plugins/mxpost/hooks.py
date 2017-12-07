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

randfactor=0.25885414

def getAnalysisOptions():
    nukemxterminator = getAnalysisOptionsEmptyContainer(
        pluginName = pluginName,
    )
    nukemxterminator['text'] = _('Delete processed data [MXTERMINATOR]')
    nukemxterminator['icon'] = 'close'
    nukemxterminator['priority'] = -2000+randfactor
    nukemxterminator['link'] = pluginName+'_sentences_nuke'
    nukemxterminator['color'] = COLOR.RED
    #
    processmxterminator = getAnalysisOptionsEmptyContainer(
        pluginName = pluginName,
    )
    processmxterminator['text'] = _('Process Corpus [MXTERMINATOR]')
    processmxterminator['icon'] = 'arrow-right'
    processmxterminator['priority'] = -1000+randfactor
    processmxterminator['link'] = pluginName+'_sentences_process'
    processmxterminator['color'] = COLOR.GREEN
    #
    mxterminator = getAnalysisOptionsEmptyContainer(
        pluginName = pluginName,
    )
    mxterminator['text'] = _('Sentence List [MXTERMINATOR]')
    mxterminator['icon'] = 'list'
    mxterminator['priority'] = 15+randfactor
    mxterminator['link'] = pluginName+'_sentences'
    #
    #
    nukemxpost = getAnalysisOptionsEmptyContainer(
        pluginName = pluginName,
    )
    nukemxpost['text'] = _('Delete processed data [MXPOST]')
    nukemxpost['icon'] = 'close'
    nukemxpost['priority'] = -2000+randfactor+.0000001
    nukemxpost['link'] = pluginName+'_tags_nuke'
    nukemxpost['color'] = COLOR.RED
    #
    processmxpost = getAnalysisOptionsEmptyContainer(
        pluginName = pluginName,
    )
    processmxpost['text'] = _('Process Corpus [MXPOST]')
    processmxpost['icon'] = 'arrow-right'
    processmxpost['priority'] = -1000+randfactor+.0000001
    processmxpost['link'] = pluginName+'_tags_process'
    processmxpost['color'] = COLOR.GREEN
    #
    mxpost = getAnalysisOptionsEmptyContainer(
        pluginName = pluginName,
    )
    mxpost['text'] = _('Tagged Text [MXPOST]')
    mxpost['icon'] = 'tags'
    mxpost['priority'] = 195+randfactor
    mxpost['link'] = pluginName+'_tags'
    return [
        nukemxterminator,
        processmxterminator,
        mxterminator,
        nukemxpost,
        processmxpost,
        mxpost,
    ]

def defaultMxterminatorAsset():
    return {
        'id':'en-us-default',
        'lang': 'en-us',
        'langfull': _('English (US)'),
        'source': 'MXPOST',
        'dir': os.path.join(os.path.dirname(os.path.abspath(__file__)),'tagger','mxpost','eos.project'),
    }

def defaultMxpostAsset():
    return {
        'id':'en-us-default',
        'lang': 'en-us',
        'langfull': _('English (US)'),
        'source': 'MXPOST',
        'dir': os.path.join(os.path.dirname(os.path.abspath(__file__)),'tagger','mxpost','tagger.project'),
    }

import json
from django.urls import reverse
from django.http import HttpResponseRedirect
importline1 = 'import '+('.'.join(['plugins',pluginName,'models'])+' as models')
exec(importline1) #import plugins.thisplugin.models as models

def getSentenceList(corpus):
    val = None
    try:
        val = json.loads(models.CorpusMxterminated.objects.get(corpus__pk=corpus.pk).sentences)
    except:
        val = HttpResponseRedirect(reverse(pluginName+'_sentences_process',None,[corpus.pk]))
    return {
        'key': pluginName,
        'name': 'MXTERMINATOR',
        'sentences': val,
    }

def getSentenceTagged(corpus):
    val = None
    try:
        val = json.loads(models.CorpusMxposted.objects.get(corpus__pk=corpus.pk).postags)
    except:
        val = HttpResponseRedirect(reverse(pluginName+'_tags_process',None,[corpus.pk]))
    return {
        'key': pluginName,
        'name': 'MXPOST',
        'sentences': val,
    }


def getHooks():
    return {
        'provider:mxterminator:asset':[
            defaultMxterminatorAsset
        ],
        'provider:mxpost:asset':[
            defaultMxpostAsset
        ],
        'query:sentencelist':[
            getSentenceList
        ],
        'query:sentencetokenstagged':[
            getSentenceTagged
        ],
    }
