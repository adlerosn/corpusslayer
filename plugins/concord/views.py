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

import corpusslayer.events as app_events

importline3 = 'import '+('.'.join(['plugins',pluginName,'searcher'])+' as searcher')
exec(importline3) #import plugins.thisplugin.searcher as searcher

# Create your views here.

class ConcordView(TemplateViewLoggedIn):
    template_name='plugins/concord/search.html'
    def get(self, request, corpus_pk='0'):
        bl = app_ctrl.Business(request)
        corpus = app_models.Corpus.objects.get(user__id=bl.user.id, pk=corpus_pk)
        form = forms.SearchForm(request.GET)
        tagsources = app_events.fire('query:sentencetokenstagged', corpus)
        taggerChoices = [(tagsource['key'], tagsource['name']) for tagsource in tagsources]
        form['tagged_corpus'].field._set_choices([('',_('Click here to select a tagger')), ('','--------')]+taggerChoices)
        return render(request, self.template_name, {
            'corpus_pk':corpus_pk,
            'form':form,
        })
    def post(self, request, corpus_pk='0'):
        bl = app_ctrl.Business(request)
        corpus = app_models.Corpus.objects.get(user__id=bl.user.id, pk=corpus_pk)
        form = forms.SearchForm(request.POST)
        tagsources = app_events.fire('query:sentencetokenstagged', corpus)
        taggerChoices = [(tagsource['key'], tagsource['name']) for tagsource in tagsources]
        form['tagged_corpus'].field._set_choices(taggerChoices)
        if not form.is_valid():
            request.GET = request.POST
            return self.get(request,corpus_pk)
        nv = int(form.cleaned_data['neighborhood_visibility'])
        tagset = None
        tagsetId = form.cleaned_data['tagged_corpus']
        for tagsource in tagsources:
            if tagsource['key'] == tagsetId:
                tagset = tagsource['sentences']
                break
        if isinstance(tagset, HttpResponseRedirect):
            return app_events.nextGetArg(tagset,request.path+app_events.buildNextGetPart(request.GET.get('next','')))
        query = form.cleaned_data['query']
        results = searcher.search(query, tagset, nv)
        return render(request, 'plugins/concord/search_results.html', {'results':results})
