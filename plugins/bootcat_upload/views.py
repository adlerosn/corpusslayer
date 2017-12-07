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

# Create your views here.

class ImporterView(TemplateViewLoggedIn):
    template_name='plugins/bootcat_upload/importUploaded.html'
    def get(self, request, corpus_pk='0'):
        bl = app_ctrl.Business(request)
        corpus = app_models.Corpus.objects.get(user__id=bl.user.id, pk=corpus_pk)
        return render(request, self.template_name, {
            'corpus': corpus,
        })
    def post(self, request, corpus_pk='0'):
        bl = app_ctrl.Business(request)
        corpus = app_models.Corpus.objects.get(user__id=bl.user.id, pk=corpus_pk)
        bcc = str(request.POST.get('corpus','')).splitlines()
        newCopus = list()
        newDocument = list()
        for line in bcc:
            if line.startswith('CURRENT URL '):
                newDocument = [ln.strip() for ln in newDocument if len(ln.strip())>0]
                newCopus.append(newDocument)
                newDocument = list()
            newDocument.append(line)
        newCopus.append(newDocument)
        newCopus = {document[0][12:]:'\n'.join(document[1:]) for document in newCopus if len(document)>1}
        newCopus = sorted(newCopus.items())
        lastError = None
        for item in newCopus:
            try:
                doc = app_models.Document(
                    ip = bl._ip,
                    user = bl.user,
                    corpus = corpus,
                    source = item[0].strip()[:255],
                    text = item[1].strip(),
                    title = item[1].strip().split('\n',1)[0].strip()[:255]
                )
                doc.save()
            except Exception as e:
                lastError = e
        if lastError:
            raise lastError
        return HttpResponseRedirect(reverse('corpus', None, [corpus_pk]))
