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
importline1 = 'import '+('.'.join(['plugins',pluginName,'models'])+' as models')
importline2 = 'import '+('.'.join(['plugins',pluginName,'forms'])+' as forms')
exec(importline1) #import plugins.thisplugin.models as models
exec(importline2) #import plugins.thisplugin.forms as forms

import application.forms as app_forms
import application.models as app_models
import application.business as app_ctrl

from django.utils.translation import ugettext_lazy as _

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View
from django.views.generic import TemplateView
from django.template.response import TemplateResponse
from django.http import Http404
from django.urls import reverse
from django.core.paginator import Paginator
from urllib.parse import urlencode

from view.pages.views import SoonView, TemplateViewLoggedIn, UserPartEditFormView
from view.pages.views import CrudDeleteView, CrudEditView, CrudListView

import re
import json
import base64

def escapeRegex(s):
    o = ''
    for c in s:
        if c in ',.+*?|^$[]{}()\\':
            o+='\\'
        o+=c
    return o

def findFirstStringAtZero(el):
    if isinstance(el,str):
        return el
    else:
        return findFirstStringAtZero(el[0])

class MockRegexSeachWithIn:
    def __init__(self, data):
        self.data = data
    def search(self, bigger):
        if bigger.__contains__(self.data):
            return True
        return None

# Create your views here.

class DocumentView(TemplateViewLoggedIn):
    template_name = 'plugins/base/document.html'
    def get(self, request, corpus_pk='0', doc_pk='0'):
        bl = app_ctrl.Business(request)
        document = app_models.Document.objects.get(user__id=bl.user.id, corpus__pk=corpus_pk, pk=doc_pk)
        corpus = document.corpus
        return render(request, self.template_name, {
            'corpus': corpus,
            'document': document,
            'textlines': document.text.strip().splitlines(),
        })

class FinderView(TemplateViewLoggedIn):
    template_name = 'plugins/base/finder.html'
    def get(self, request, corpus_pk='0', fragment=''):
        bl = app_ctrl.Business(request)
        corpus = app_models.Corpus.objects.get(user__id=bl.user.id, pk=corpus_pk)
        documents = corpus.documents.all()
        wanted = json.loads(base64.b64decode(fragment).decode('utf-8'))
        searched = None
        if isinstance(wanted,str):
            searched = escapeRegex(wanted.strip())
            searched = searched.replace(' ','\\s*')
            wanted = re.compile(searched)
        else:
            searched = '\\s*'.join(map(escapeRegex, map(findFirstStringAtZero, wanted)))
            wanted = re.compile(searched)
        matchedDocs = list()
        for document in documents:
            if wanted.search(document.text) is not None:
                matchedDocs.append(document)
        matchedDocs.sort(key=lambda a: a.title)
        if len(matchedDocs)<=0:
            raise Http404("Couldn't find any document with: "+searched)
        if len(matchedDocs)==1:
            return HttpResponseRedirect(reverse('base_document',None,[corpus_pk,matchedDocs[0].pk]))
        return render(request, self.template_name, {
            'query':searched,
            'corpus':corpus,
            'documents':matchedDocs,
        })
