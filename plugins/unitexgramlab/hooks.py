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

randfactor = .1494648

def getAnalysisOptions():
    dropcache = getAnalysisOptionsEmptyContainer(
        pluginName = pluginName,
    )
    dropcache['text'] = _('Delete processed data [Unitex/GramLab]')
    dropcache['priority'] = -2000+randfactor
    dropcache['icon'] = 'close'
    dropcache['link'] = pluginName+'_nuke'
    dropcache['color'] = COLOR.RED
    createcache = getAnalysisOptionsEmptyContainer(
        pluginName = pluginName,
    )
    createcache['text'] = _('Process Corpus [Unitex/GramLab]')
    createcache['priority'] = -1000+randfactor
    createcache['icon'] = 'arrow-right'
    createcache['link'] = pluginName+'_process'
    createcache['color'] = COLOR.GREEN
    sentences = getAnalysisOptionsEmptyContainer(
        pluginName = pluginName,
    )
    sentences['text'] = _('Sentence List [Unitex/GramLab]')
    sentences['priority'] = 10+randfactor
    sentences['icon'] = 'list'
    sentences['link'] = pluginName+'_sentences'
    wordfreq = getAnalysisOptionsEmptyContainer(
        pluginName = pluginName,
    )
    wordfreq['text'] = _('Word Frequency [Unitex/GramLab]')
    wordfreq['priority'] = 20+randfactor
    wordfreq['icon'] = 'list-ol'
    wordfreq['link'] = pluginName+'_wordfreq'
    wordlist = getAnalysisOptionsEmptyContainer(
        pluginName = pluginName,
    )
    wordlist['text'] = _('Word List [Unitex/GramLab]')
    wordlist['priority'] = 25+randfactor
    wordlist['icon'] = 'list-ul'
    wordlist['link'] = pluginName+'_wordlist'
    sntauto = getAnalysisOptionsEmptyContainer(
        pluginName = pluginName,
    )
    sntauto['text'] = _('Sentence Automata [Unitex/GramLab]')
    sntauto['priority'] = 30+randfactor
    sntauto['icon'] = 'reorder'
    sntauto['link'] = pluginName+'_sntauto'
    txtauto = getAnalysisOptionsEmptyContainer(
        pluginName = pluginName,
    )
    txtauto['text'] = _('Text Automata [Unitex/GramLab]')
    txtauto['priority'] = 30+randfactor
    txtauto['icon'] = 'sliders'
    txtauto['link'] = pluginName+'_txtauto'
    return [
        dropcache,
        createcache,
        sentences,
        wordfreq,
        wordlist,
        sntauto,
        txtauto,
    ]

import json
from django.urls import reverse
from django.http import HttpResponseRedirect
importline1 = 'import '+('.'.join(['plugins',pluginName,'models'])+' as models')
exec(importline1) #import plugins.thisplugin.models as models

def getSentenceList(corpus):
    val = None
    try:
        val = json.loads(models.CorpusProcessed.objects.get(corpus__pk=corpus.pk).sentences)
        val = list(filter(lambda l: len(l)>0, val))
        if len(val)==0:
            raise Exception()
    except:
        val = HttpResponseRedirect(reverse(pluginName+'_process',None,[corpus.pk]))
    return {
        'key': pluginName,
        'name': 'Unitex/GramLab',
        'sentences': val,
    }

def getSentenceTokens(corpus):
    val = None
    try:
        val = json.loads(models.CorpusProcessed.objects.get(corpus__pk=corpus.pk).fsttext)
        val = [
            [
                palavra
                for palavra in sentence['componentes']
                if palavra.isprintable() and not palavra.isspace()
            ]
            for sentence in val
        ]
    except:
        val = HttpResponseRedirect(reverse(pluginName+'_process',None,[corpus.pk]))
    return {
        'key': pluginName,
        'name': 'Unitex/GramLab',
        'sentences': val,
    }
_('Unitex/GramLab (tags are empty)')
def getSentenceTokensTagged(corpus):
    tok = getSentenceTokens(corpus)
    tok['name']=_(tok['name']+' (tags are empty)')
    if not isinstance(tok['sentences'], HttpResponseRedirect):
        tok['sentences'] = [[[word, ''] for word in sentence] for sentence in tok['sentences']]
    return tok;

def getHooks():
    return {
        'query:sentencelist':[
            getSentenceList
        ],
        'query:sentencetokens':[
            getSentenceTokens
        ],
        'query:sentencetokenstagged':[
            getSentenceTokensTagged
        ],
    }
