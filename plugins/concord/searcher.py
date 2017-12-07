#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

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

import sys

def mocksearch(query, taggedSentences):
    resultado = {
            'sentence':[['A','ART'],['casa','N'],['é','V'],['vermelha','N'],],
            'match':[['casa','N'],],
    }
    return [resultado,resultado]

class SearchException(Exception): pass
class SearchQueryException(SearchException): pass

import math

#direct translation from JS code; forgive me if the code stinks
def backslashUnescaper(stri):
    escape = False
    escaped = ''
    for char in stri:
        if escape:
            escape=False;
            escaped+=char;
        else:
            if char=='\\':
                escape=True;
            else:
                escaped+=char;
    return escaped

#direct translation from JS code; forgive me if the code stinks
def backslashRemovingEscaped(stri):
    escape = False
    escaped = ''
    for char in stri:
        if escape:
            escape=False;
        else:
            if char=='\\':
                escape=True;
            else:
                escaped+=char;
    return escaped

def parseInt(var=None):
    try:
        return int(var)
    except:
        return math.nan

def isNaN(var=None):
    if var is None or math.isnan(var):
        return True
    else:
        return False

#direct translation from JS code; forgive me if the code stinks
def interpretRange(stri, conc=None):
    conclusion={
        'type':'fragment',
        'text':[]
    }
    if conc is not None:
        conclusion = conc
    conclusion['type']='skip'
    rangi = list(map(parseInt,stri[1:-1].split(',')[:2]))
    if(
        len(rangi)>1
        and
        (
            rangi[0]==rangi[1]
            or
            (
                isNaN(rangi[0])
                and
                isNaN(rangi[1])
            )
        )
    ):
        rangi = rangi[:1]
    if len(rangi)==1 and isNaN(rangi[0]):
        rangi = [0,rangi[0]]
    if len(rangi)>1:
        conclusion['type']+='range'
    for i in range(len(rangi)):
        if isNaN(rangi[i]):
            rangi[i]='any'
    if len(rangi)>1 and rangi[0]=='any':
        rangi[0] = 0
    conclusion['text'] = rangi;
    return conclusion

import re

regex_ul = re.compile(r'\?([UL])({[0-9,* ]+})?')
regex_be = re.compile(r'^([^.]+)\.\.')
regex_mi = re.compile(r'\.\.([^.]+)\.\.')
regex_en = re.compile(r'\.\.([^.]+)$')

#direct translation from JS code; forgive me if the code stinks
def parseQuery(typed):
    parts = list(map(lambda a: a.split('__'), list(filter(lambda a: a!='', typed.split(' ')))))
    for part_ndx, _ in enumerate(parts):
        text = parts[part_ndx][0];
        visible = backslashRemovingEscaped(text)
        conclusion = {
            'type':'plain',
            'text':[backslashUnescaper(text)]
        }
        if text=='':
            conclusion['type']='ignore'
            conclusion['text']=[]
        elif text.find('..')>=0:
            begin = regex_be.search(text)
            middle = regex_mi.search(text)
            end = regex_en.search(text)
            conclusion['type']='fragment'
            conclusion['text']=[]
            if begin:
                conclusion['text'].append(['starts with',backslashUnescaper(begin.groups()[0])])
            if middle:
                conclusion['text'].append(['contains',backslashUnescaper(middle.groups()[0])])
            if end:
                conclusion['text'].append(['ends with',backslashUnescaper(end.groups()[0])])
        elif len(visible)>0 and visible[0]=='{' and visible[-1]=='}':
            conclusion = interpretRange(visible,conclusion)
        '''
        elif text.find('?U')>=0 or text.find('?L')>=0:
            conclusion['type']='cases'
            conclusion['text']=[]
            remain = text
            while len(remain)>0:
                nextMatch = regex_ul.search(remain)
                if nextMatch:
                    matchedData = nextMatch.string[nextMatch.start(0):nextMatch.end(0)]
                    nextMatch = nextMatch.groups()
                    nextMatch = [matchedData]+list(nextMatch)
                    toConsume = remain.find(nextMatch[0])
                    if toConsume>0:
                        conclusion['text'].append([
                            'plain',
                            backslashUnescaper(remain[0:toConsume])
                        ]);
                        remain = remain[toConsume:]
                    tcase = None
                    if nextMatch[1]=='U':
                        tcase = 'uppercase'
                    else:
                        tcase = 'lowercase'
                    irange = interpretRange('{1}')
                    if nextMatch[2]:
                        irange = interpretRange(nextMatch[2])
                    conclusion['text'].append([
                        'casefind',
                        tcase,
                        irange['text']
                    ])
                    remain = remain[len(nextMatch[0]):]
                else:
                    conclusion['text'].append([
                        'plain',
                        backslashUnescaper(remain)
                    ])
                    remain = ''
        '''
        parts[part_ndx][0] = conclusion
    return parts

def aux_skipAdd(val1,val2):
    if val1=='any' or val2=='any':
        return 'any'
    else:
        return val1+val2

def aux_skipNormalize(val):
    if len(val)==1:
        return [val[0], val[0]]
    return val

def aux_skipToRange(val,padding,limit):
    v = aux_skipNormalize(val)
    if v[1]=='any':
        v[1]=limit
    return range(min(padding+v[0],limit),min(padding+v[1],limit))

def aux_skipReduce(val):
    if val[0] == val[1]:
        return [val[0]]
    return val

def aux_sumSkips(skip1, skip2):
    val = {'type':'skip','text':[]}
    toSum = list(zip(aux_skipNormalize(skip1['text']),aux_skipNormalize(skip2['text'])))
    txt = aux_skipReduce([aux_skipAdd(*i) for i in toSum])
    if len(txt)>1:
        val['type']+='range'
    val['text']=txt
    return val

def optimizeSkips(parsed):
    i = 0
    while i+1<len(parsed):
        if parsed[i][0]['type'].startswith('skip') and parsed[i+1][0]['type'].startswith('skip'):
            optimized = aux_sumSkips(parsed[i][0],parsed[i+1][0])
            del parsed[i+1]
            parsed[i]=[optimized]
            i-=1
        i+=1
    return parsed

class ResultRanges(object):
    positions = []
    currentPos = 0
    def setCurrentPos(self,v):
        self.currentPos = v
    def push(self,v):
        self.positions.append((self.currentPos,v))
    def reset(self):
        self.positions = list()

class StepFinderIgnore(object):
    def __init__(self, _next=None, headcheck=None, tagcheck=None):
        self._next = _next
        self.ranges = ResultRanges()
        if headcheck is None:
            headcheck = list()
        self.headcheck = headcheck
        if tagcheck is None:
            tagcheck = list()
        self.tagcheck = tagcheck
    def test(self, taggedSentence):
        self.ranges.reset()
        for i in range(len(taggedSentence)):
            self.ranges.setCurrentPos(i)
            self._test(taggedSentence, self.ranges,i)
        return self.results
    def _test(self, taggedSentence, manager, current):
        if current not in range(len(taggedSentence)):
            return
        for test in self._getTests(taggedSentence,current):
            pos = test()
            if pos:
                if self._checkTags(pos,taggedSentence):
                    if self._next:
                        self._next._test(taggedSentence, manager, pos+1)
                    else:
                        manager.push(pos+1)
    def _checkTags(self, pos, taggedSentence):
        if pos not in range(len(taggedSentence)):
            return False
        if len(self.tagcheck):
            return taggedSentence[pos][1] in self.tagcheck
        else:
            return True
    def _getTests(self, *args):
        return [lambda: True]
    @property
    def results(self):
        return self.ranges.positions

class StepFinderPlain(StepFinderIgnore):
    def _getTests(self, taggedSentence, current):
        return [
            lambda: int(self.headcheck[0]==taggedSentence[current][0])*current
        ]

class StepFinderFragment(StepFinderIgnore):
    def _getTests(self, taggedSentence, current):
        keys = {
                'starts with': lambda a: taggedSentence[current][0].startswith(a),
                'contains':lambda a: taggedSentence[current][0].__contains__(a),
                'ends with':lambda a: taggedSentence[current][0].endswith(a),
        }
        return [
            lambda: int(all([
                keys[check[0]](check[1])
                for check in self.headcheck
            ]))*current
        ]

class returnsGiven:
    def __init__(self, toSave):
        self.saved = toSave
    def __call__(self):
        return self.saved

class StepFinderSkip(StepFinderIgnore):
    def _getTests(self, taggedSentence, current):
        newpos = [returnsGiven(x) for x in aux_skipToRange(self.headcheck,current, len(taggedSentence))]
        return newpos

def buildClasses(query):
    curr = None
    for part in query[::-1]:
        args = [curr, part[0]['text'], part[1:]]
        if part[0]['type'] == 'ignore':
            curr = StepFinderIgnore(*args)
        elif part[0]['type'] == 'plain':
            curr = StepFinderPlain(*args)
        elif part[0]['type'] == 'fragment':
            curr = StepFinderFragment(*args)
        elif part[0]['type'].startswith('skip'):
            curr = StepFinderSkip(*args)
        else:
            raise SearchQueryException('Couldn\'t locate type: '+str(part['type']))
    return curr

def search(query, taggedSentences, context = -1):
    if len(query)<=0: return list()
    tag = optimizeSkips(parseQuery(query))
    searcher = buildClasses(tag)
    results = list()
    for taggedSentence in taggedSentences:
        ranges = searcher.test(taggedSentence)
        for rng in ranges:
            if rng[0] >= rng[1]:
                continue
            matches = taggedSentence[rng[0]:rng[1]]
            r = range(rng[0],rng[1])
            if len(matches)<=0:
                continue
            hintedFragment = None
            hintedSentence = [[word,tag,i in r] for (i, (word, tag)) in enumerate(taggedSentence)]
            if context == 0:
                hintedFragment = [[word,tag,True] for word, tag in matches]
            elif context < 0:
                hintedFragment = hintedSentence
            else:
                lr = rng[0]
                ur = rng[1]
                lr-=context
                ur+=context
                lr = max(0,lr)
                ur = min(ur,len(hintedSentence))
                hintedFragment = hintedSentence[lr:ur]
            results.append({
                'excerpt': rng,
                'excerptInc': [rng[0]+1, rng[1]+1],
                'sentence': taggedSentence,
                'match': matches,
                'hintedSentence': hintedSentence,
                'fragsize':context,
                'hintedFragment': hintedFragment,
            })
    return results
