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
import json

from view.pages.views import SoonView, TemplateViewLoggedIn, UserPartEditFormView
from view.pages.views import CrudDeleteView, CrudEditView, CrudListView

import corpusslayer.events as app_events

importline3 = 'from '+('.'.join(['plugins',pluginName,'unitexgramlab','unitexActions'])+' import UnitexActions')
exec(importline3) #from plugins.thisplugin.unitexgramlab.unitexActions import UnitexActions

dummyUnitex = UnitexActions.get_dumb_one()

unitexProcesses = dict()

import concurrent.futures

taskPool = concurrent.futures.ThreadPoolExecutor(max_workers=65535)

# Create your views here.

def getProcessedCacheOrRedirect(corpus,reqpath):
    try:
        cached = corpus.__getattribute__(pluginName+'_cache')
        if cached.modified < corpus.modifiedWithChild:
            raise Exception('Cache is invalid')
    except:
        return HttpResponseRedirect(reverse(pluginName+'_process',None,[corpus.pk])+app_events.buildNextGetPart(reqpath))
    return corpus.__getattribute__(pluginName+'_cache')

class NukeView(TemplateViewLoggedIn):
    template_name = 'plugins/unitexgramlab/sentences.html'
    def get(self, request, corpus_pk='0'):
        bl = app_ctrl.Business(request)
        corpus = app_models.Corpus.objects.get(user__id=bl.user.id, pk=corpus_pk)
        processed = getProcessedCacheOrRedirect(corpus,request.path)
        if not isinstance(processed, HttpResponseRedirect):
            processed.delete()
        return HttpResponseRedirect(reverse('analysis', None, corpus_pk))

#default
_('Arabic')
_('English')
_('Finnish')
_('French')
_('Georgian (Ancient)')
_('German')
_('Greek (Ancient)')
_('Greek (Modern)')
_('Italian')
_('Korean')
_('Latin')
_('Malagasy')
_('Norwegian (Bokmal)')
_('Norwegian (Nynorsk)')
_('Polish')
_('Portuguese (Brazil)')
_('Portuguese (Portugal)')
_('Russian')
_('Serbian-Cyrillic')
_('Serbian-Latin')
_('Spanish')
_('Thai')
class ProcessView(TemplateViewLoggedIn):
    template_name = 'plugins/unitexgramlab/process.html'
    def get(self, request, corpus_pk='0'):
        bl = app_ctrl.Business(request)
        corpus = app_models.Corpus.objects.get(user__id=bl.user.id, pk=corpus_pk)
        form = forms.ProcessForm(initial=request.GET)
        langChoices = sorted(dummyUnitex.langNameFs.items(), key=lambda pair: pair[0]),
        langChoices = [(k,_(v)) for k,v in langChoices[0]]
        form['language'].field._set_choices([('',_('Click here to select a language')), ('','--------')]+langChoices)
        return render(request, self.template_name, {
            'form': form,
        })
    def post(self, request, corpus_pk='0'):
        global unitexProcesses
        bl = app_ctrl.Business(request)
        corpus = app_models.Corpus.objects.get(user__id=bl.user.id, pk=corpus_pk)
        form = forms.ProcessForm(request.POST)
        langChoices = sorted(dummyUnitex.langNameFs.items(), key=lambda pair: pair[1])
        form['language'].field._set_choices(langChoices)
        if not form.is_valid():
            request.GET = request.POST
            return self.get(request,corpus_pk)

        ua = UnitexActions(**{
            'corpus_content': corpus.mergedDocuments,
            'lang': form.cleaned_data['language'],
        })
        jobPk = int(ua.id)
        ua.planPreprocessing()
        ua.planFstText()
        if not form.cleaned_data['skip_text_automata']:
            ua.planSequenceAutomata()
        unitexProcesses[jobPk] = {
            'object': ua,
            'thread': taskPool.submit(ua.executePlanning),
        }
        return HttpResponseRedirect(reverse(pluginName+'_job_wait',None,[corpus_pk,jobPk])+app_events.buildNextGetPart(request.GET.get('next','')))

#steps
_('preprocessing_normalize_input')
_('preprocessing_converting_graph')
_('preprocessing_flattening_graph')
_('preprocessing_plainifying_graph')
_('preprocessing_converting_graph_again')
_('preprocessing_flattening_graph_again')
_('preprocessing_extracting_tokens')
_('preprocessing_using_dictionary')
_('preprocessing_sorting_text_simple')
_('preprocessing_sorting_text_compound')
_('preprocessing_sorting_text_unknown')
_('preprocessing_sorting_text_unknown_unique')
_('preprocessing_wordlist_parsing')
_('preprocessing_wordlist_parsing')
_('preprocessing_wordfreq_parsing')
_('preprocessing_sentences_parsing')
_('converting_fst_graph')
_('building_fst_text')
_('parsing_fst_text')
_('parsing_fst_tagfreq')
_('tagging_fst_text')
_('parsing_fst_text_tagged')
_('parsing_fst_taggedfreq')
_('seq_auto_process')
_('seq_auto_parsing')
class JobWaiterView(TemplateViewLoggedIn):
    template_name = 'plugins/unitexgramlab/wait.html'
    def get(self, request, corpus_pk='0', job_pk='0'):
        global unitexProcesses
        bl = app_ctrl.Business(request)
        corpus = app_models.Corpus.objects.get(user__id=bl.user.id, pk=corpus_pk)
        corpus_pk = int(corpus_pk)
        job_pk = int(job_pk)
        finishedLink = reverse('analysis', None, [corpus_pk])
        if(request.GET.get('next', False)):
            finishedLink = request.GET['next']
        try:
            unitexProcesses[job_pk]
        except KeyError:
            return HttpResponseRedirect(finishedLink)
        object = unitexProcesses[job_pk]['object']
        thread = unitexProcesses[job_pk]['thread']
        finished = thread.done()
        logs = object.status['logs']
        if finished:
            models.CorpusProcessed.objects.filter(user__id=bl.user.id, corpus__pk=corpus_pk).delete()
            proc = models.CorpusProcessed(**{k:json.dumps(v) for k,v in object._jsonable['results'].items()})
            proc.corpus = corpus
            proc.user = bl.user
            proc.save()
            finished = finishedLink
            object.delete()
            del unitexProcesses[job_pk]
        pf = 0
        try:
            pf = int(100 * logs['current_length'] / logs['expected_length'])
        except: pass
        return render(request, self.template_name, {
            'logs': logs,
            'percent_finished': pf,
            'finished': finished,
            'corpus_pk': corpus_pk,
        })

class SentenceListView(TemplateViewLoggedIn):
    template_name = 'plugins/unitexgramlab/sentences.html'
    def get(self, request, corpus_pk='0'):
        bl = app_ctrl.Business(request)
        corpus = app_models.Corpus.objects.get(user__id=bl.user.id, pk=corpus_pk)
        processed = getProcessedCacheOrRedirect(corpus,request.path)
        if isinstance(processed, HttpResponseRedirect): return processed
        sentences = json.loads(processed.sentences)
        return render(request, self.template_name, {
            'sentences': sentences,
        })

class WordFreqView(TemplateViewLoggedIn):
    template_name = 'plugins/unitexgramlab/wordfreq.html'
    def get(self, request, corpus_pk='0'):
        bl = app_ctrl.Business(request)
        corpus = app_models.Corpus.objects.get(user__id=bl.user.id, pk=corpus_pk)
        processed = getProcessedCacheOrRedirect(corpus,request.path)
        if isinstance(processed, HttpResponseRedirect): return processed
        words = sorted(json.loads(processed.wordfreq).items(),
            key = lambda a: (-a[1],a[0])
        )
        return render(request, self.template_name, {
            'words': words,
        })

class WordListView(TemplateViewLoggedIn):
    template_name = 'plugins/unitexgramlab/wordlist.html'
    def get(self, request, corpus_pk='0'):
        bl = app_ctrl.Business(request)
        corpus = app_models.Corpus.objects.get(user__id=bl.user.id, pk=corpus_pk)
        processed = getProcessedCacheOrRedirect(corpus,request.path)
        if isinstance(processed, HttpResponseRedirect): return processed
        words = json.loads(processed.wordlist)
        composto = words['composto']
        simples = words['simples']
        naoReconhecido = words['naoReconhecido']
        return render(request, self.template_name, {
            'words': words,
            'simples': simples,
            'composto': composto,
            'naoReconhecido': naoReconhecido,
        })

class SentenceAutomatonView(TemplateViewLoggedIn):
    template_name = 'plugins/unitexgramlab/sentenceautomaton.html'
    def get(self, request, corpus_pk='0'):
        bl = app_ctrl.Business(request)
        corpus = app_models.Corpus.objects.get(user__id=bl.user.id, pk=corpus_pk)
        processed = getProcessedCacheOrRedirect(corpus,request.path)
        if isinstance(processed, HttpResponseRedirect): return processed
        sentences = json.loads(processed.fsttext)
        for i,sentence in enumerate(sentences):
            d = dict()
            for i, no in sentence['grafoLinear']:
                if i not in d:
                    d[i] = list()
                d[i].append(no)
            l = list(sorted(map(list, d.items())))
            sentence['grafoLinear'] = l
            if(len(l)>0):
                sentence['grafoLinear'][len(l)-1].append(True)
        return render(request, self.template_name, {
            'sentences': sentences,
        })

import uuid
import graphviz
import subprocess
import base64

class TextAutomatonView(TemplateViewLoggedIn):
    template_name = 'plugins/unitexgramlab/txtauto.html'
    def get(self, request, corpus_pk='0'):
        bl = app_ctrl.Business(request)
        corpus = app_models.Corpus.objects.get(user__id=bl.user.id, pk=corpus_pk)
        processed = getProcessedCacheOrRedirect(corpus,request.path)
        if isinstance(processed, HttpResponseRedirect): return processed
        jpgContent = None
        if not hasattr(processed, 'text_automaton_rendered'):
            txtauto = json.loads(processed.aec)
            if txtauto is None:
                return HttpResponseRedirect(reverse(pluginName+'_txtauto_missing', None, [corpus_pk]))
            gid = uuid.uuid4()
            grf = graphviz.Digraph(
                name=str(gid),
                format='svg',
                encoding='utf-8',
                engine='sfdp',
                comment='Autogenerated using UTF-8 charset'
            )
            grf.attr(rankdir='LR')
            grf.attr(shape='box')
            grf.attr(fillcolor='white')
            grf.attr(outputorder='edgesfirst')
            grf.attr(concentrate='true')
            rescaleFactor = 40
            grf.node(
                str(txtauto[0]['local_id']),
                txtauto[0]['conteudo'],
                fillcolor='#00FF00',
                shape='doublecircle',
                pos=str(txtauto[0]['arestaPara'][0]/rescaleFactor)+','+str(txtauto[0]['arestaPara'][1]/rescaleFactor)+'!'
            )
            grf.node(
                str(txtauto[1]['local_id']),
                txtauto[1]['conteudo'],
                fillcolor='#FFFF00',
                shape='doublecircle',
                pos=str(txtauto[1]['arestaPara'][0]/rescaleFactor)+','+str(txtauto[1]['arestaPara'][1]/rescaleFactor)+'!'
            )
            for item in txtauto[2:]:
                grf.node(
                    str(item['local_id']),
                    item['conteudo'],
                    pos=str(item['arestaPara'][0]/rescaleFactor)+','+str(item['arestaPara'][1]/rescaleFactor)+'!'
                )
            for este in txtauto:
                for outro in este['arestaPara'][2:]:
                    grf.edge(str(este['local_id']), str(outro))
            #raise Exception(txtauto)
            #return HttpResponse(grf.source, content_type='text/plain')
            if len(txtauto)>=1000:
                return render(request, 'plugins/unitexgramlab/txtauto_huge.html', {
                    'corpus': corpus,
                    'commands': [
                        'sfdp -Kfdp -Goverlap=scale -Tsvg -O "%s.gv"'%(corpus.title),
                        'sfdp -Kfdp -Goverlap=scale -Tpdf -O "%s.gv"'%(corpus.title),
                        'sfdp -Kfdp -Goverlap=scale -Tjpg -O "%s.gv"'%(corpus.title),
                    ],
                    'dotfile': grf.source,
                    'dotfileb64': base64.b64encode(grf.source.encode()),
                })
            svgResult = subprocess.run(
                ['sfdp', '-Kfdp', '-Goverlap=scale', '-Tsvg'],
                input=grf.source.encode(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            pdfResult = subprocess.run(
                ['sfdp', '-Kfdp', '-Goverlap=scale', '-Tpdf'],
                input=grf.source.encode(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            jpgResult = subprocess.run(
                ['sfdp', '-Kfdp', '-Goverlap=scale', '-Tjpg'],
                input=grf.source.encode(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            svgContent = svgResult.stdout
            pdfContent = pdfResult.stdout
            jpgContent = jpgResult.stdout
            gvContent = grf.source.encode()
            models.TextAutomatonCache.objects.filter(corpus=processed).delete()
            models.TextAutomatonCache(
                corpus=processed,
                svg=svgContent,
                pdf=pdfContent,
                jpg=jpgContent,
                gv=gvContent
            ).save()
        else:
            jpgContent = processed.text_automaton_rendered.jpg
        jpgBase64 = base64.b64encode(jpgContent)
        return render(request, self.template_name, {
            'corpus_pk': corpus_pk,
            'download': pluginName+'_txtauto_dwn',
            'jpgBase64': jpgBase64,
        })

class TextAutomatonMissingView(TemplateViewLoggedIn):
    template_name = 'plugins/unitexgramlab/txtauto_missing.html'
    def get(self, request, corpus_pk='0'):
        next = reverse(pluginName+'_txtauto',None,[corpus_pk])
        link_back = reverse(pluginName+'_process',None,[corpus_pk])+app_events.buildNextGetPart(next)+'&skip_text_automata='
        return render(request, self.template_name, {
            'corpus_pk': corpus_pk,
            'link_back': link_back,
        })

import mimetypes

class TextAutomatonDownload(TemplateViewLoggedIn):
    def get(self, request, corpus_pk='0', fmt=''):
        if fmt not in ['svg', 'jpg', 'pdf', 'gv']:
            raise Http404
        bl = app_ctrl.Business(request)
        corpus = app_models.Corpus.objects.get(user__id=bl.user.id, pk=corpus_pk)
        files = corpus.__getattribute__(pluginName+'_cache').text_automaton_rendered
        data = files.__getattribute__(fmt)
        mime = mimetypes.types_map.get('.'+fmt,'application/octet-stream')
        if(fmt=='gv'):
            mime='text/plain'
        if(fmt in ['svg', 'gv']):
            data = data.decode()
        return HttpResponse(data, content_type=mime, charset='UTF-8')
