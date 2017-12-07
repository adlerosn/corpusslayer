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
# Create your views here.

try:
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tagger', 'mxpost', 'LICENSE.html')) as f:
        htmlLicense = f.read()
except:
    raise FileNotFoundError('Run "make all" to initialize platform')

mxterminatorAssets = app_events.fire('provider:mxterminator:asset')
mxpostAssets = app_events.fire('provider:mxpost:asset')

class LicenseView(TemplateView):
    def get(self, request, **kwargs):
        return HttpResponse(htmlLicense)

import subprocess
import json

class TermProcessView(TemplateViewLoggedIn):
    template_name = 'plugins/mxpost/term_process.html'
    def get(self, request, corpus_pk='0'):
        bl = app_ctrl.Business(request)
        corpus = app_models.Corpus.objects.get(user__id=bl.user.id, pk=corpus_pk)
        return render(request, self.template_name, {
            'license_dockey': pluginName+'_license',
            'corpus_pk': corpus_pk,
            'assets': mxterminatorAssets,
        })
    def post(self, request, corpus_pk='0'):
        bl = app_ctrl.Business(request)
        corpus = app_models.Corpus.objects.get(user__id=bl.user.id, pk=corpus_pk)
        selectedId = request.POST.get('lang', '')
        lang = None
        for asset in mxterminatorAssets:
            if asset['id'] == selectedId:
                lang = asset
                break
        if lang is None or 'dir' not in lang:
            raise Http404
        runOut = subprocess.run(
            [
                os.path.join(os.path.dirname(os.path.abspath(__file__)),'tagger','mxterminator.sh'),
                lang['dir'],
            ],
            input = corpus.mergedDocuments.encode(),
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE
        )
        sentencesRaw = runOut.stdout.decode()
        sentences = sentencesRaw.splitlines()
        if(len(sentencesRaw)==0):
            secretDirs = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            return render(request,'plugins/mxpost/trace_error.html',{
                'corpus_pk': corpus_pk,
                'log': runOut.stderr.decode().replace(secretDirs,'.')
            })
        models.CorpusMxterminated.objects.filter(user__id=bl.user.id, corpus__pk=corpus_pk).delete()
        models.CorpusMxterminated(corpus=corpus,user=bl.user,sentences=json.dumps(sentences)).save()
        if(request.GET.get('next', False)):
            return HttpResponseRedirect(request.GET['next'])
        return HttpResponseRedirect(reverse('analysis',None,[corpus_pk]))

class TermNukeView(TemplateViewLoggedIn):
    def get(self, request, corpus_pk='0'):
        bl = app_ctrl.Business(request)
        corpus = app_models.Corpus.objects.get(user__id=bl.user.id, pk=corpus_pk)
        models.CorpusMxterminated.objects.filter(user__id=bl.user.id, corpus__pk=corpus_pk).delete()
        return HttpResponseRedirect(reverse('analysis',None,[corpus_pk]))

class TermSentencesView(TemplateViewLoggedIn):
    template_name = 'plugins/mxpost/term_snts.html'
    def get(self, request, corpus_pk='0'):
        bl = app_ctrl.Business(request)
        corpus = app_models.Corpus.objects.get(user__id=bl.user.id, pk=corpus_pk)
        sentences = []
        try:
            sentences = json.loads(models.CorpusMxterminated.objects.get(user__id=bl.user.id, corpus__pk=corpus_pk).sentences)
        except:
            return HttpResponseRedirect(reverse(pluginName+'_sentences_process',None,[corpus_pk])+app_events.buildNextGetPart(request.path))
        return render(request, self.template_name, {'sentences':sentences})


class PostTagProcessView(TemplateViewLoggedIn):
    template_name = 'plugins/mxpost/tags_process.html'
    def get(self, request, corpus_pk='0'):
        bl = app_ctrl.Business(request)
        corpus = app_models.Corpus.objects.get(user__id=bl.user.id, pk=corpus_pk)
        sentencers = app_events.fire('query:sentencelist', corpus)
        return render(request, self.template_name, {
            'license_dockey': pluginName+'_license',
            'corpus_pk': corpus_pk,
            'assets': mxpostAssets,
            'sources':sentencers,
        })
    def post(self, request, corpus_pk='0'):
        bl = app_ctrl.Business(request)
        corpus = app_models.Corpus.objects.get(user__id=bl.user.id, pk=corpus_pk)
        selectedId = request.POST.get('lang', '')
        lang = None
        for asset in mxpostAssets:
            if asset['id'] == selectedId:
                lang = asset
                break
        if lang is None or 'dir' not in lang:
            raise Http404
        selectedId = request.POST.get('source', '')
        sentencers = app_events.fire('query:sentencelist', corpus)
        sentences = list()
        for asset in sentencers:
            if asset['key'] == selectedId:
                sentences = asset.get('sentences',None)
                break
        if sentences is None:
            raise Http404
        if isinstance(sentences, HttpResponseRedirect):
            return app_events.nextGetArg(sentences,request.path+app_events.buildNextGetPart(request.GET.get('next','')))
        runOut = subprocess.run(
            [
                os.path.join(os.path.dirname(os.path.abspath(__file__)),'tagger','mxpost.sh'),
                lang['dir'],
            ],
            input = ('\n'.join(sentences)+'\n').encode(),
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE
        )
        tags = runOut.stdout.decode()
        if(len(tags)==0):
            secretDirs = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            return render(request,'plugins/mxpost/trace_error.html',{
                'corpus_pk': corpus_pk,
                'log': runOut.stderr.decode().replace(secretDirs,'.')
            })
        tagged = [[word.split('_',1) for word in line.split(' ') if '_' in word] for line in tags.splitlines()]
        models.CorpusMxposted.objects.filter(user__id=bl.user.id, corpus__pk=corpus_pk).delete()
        models.CorpusMxposted(corpus=corpus,user=bl.user,postags=json.dumps(tagged)).save()
        if(request.GET.get('next', False)):
            return HttpResponseRedirect(request.GET['next'])
        return HttpResponseRedirect(reverse('analysis',None,[corpus_pk]))

class PostTagNukeView(TemplateViewLoggedIn):
    def get(self, request, corpus_pk='0'):
        bl = app_ctrl.Business(request)
        corpus = app_models.Corpus.objects.get(user__id=bl.user.id, pk=corpus_pk)
        models.CorpusMxposted.objects.filter(user__id=bl.user.id, corpus__pk=corpus_pk).delete()
        return HttpResponseRedirect(reverse('analysis',None,[corpus_pk]))

class PostTagView(TemplateViewLoggedIn):
    template_name = 'plugins/mxpost/tags_snts.html'
    def get(self, request, corpus_pk='0'):
        bl = app_ctrl.Business(request)
        corpus = app_models.Corpus.objects.get(user__id=bl.user.id, pk=corpus_pk)
        postags = []
        try:
            postags = json.loads(models.CorpusMxposted.objects.get(user__id=bl.user.id, corpus__pk=corpus_pk).postags)
        except:
            return HttpResponseRedirect(reverse(pluginName+'_tags_process',None,[corpus_pk])+app_events.buildNextGetPart(request.path))
        return render(request, self.template_name, {'postags':postags})
