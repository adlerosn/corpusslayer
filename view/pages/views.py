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

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View
from django.views.generic import TemplateView
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse
from django.utils.html import escape
from django.core.paginator import Paginator

from application import views as ctrl
from application import forms

from secrets.hookModules import hookModules
analysisOptions = list()
for module in hookModules:
    if hasattr(module, 'getAnalysisOptions'):
        for entry in module.getAnalysisOptions():
            analysisOptions.append(entry)
analysisOptions.sort(key=lambda item: (item.get('priority',100), item.get('text','')))

#
# Trivial views
#

class SoonView(TemplateView):
    template_name = "soon.html"

class LegalTosView(TemplateView):
    template_name = "legal/tos.html"

class LegalPrivView(TemplateView):
    template_name = "legal/privacy.html"

class HelpView(TemplateView):
    template_name = "help.html"

#
# ABSTRACT VIEWS
#

class TemplateViewLoggedIn(TemplateView, LoginRequiredMixin):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class UserPartEditFormView(TemplateViewLoggedIn):
    '''    Edits OneToOne fields - such as profiles    '''
    form = None
    pagetitle = '??? Edit'
    template_name = "forms/form.html"
    on_success = 'index'
    on_success_args = []
    on_success_kwargs = {}
    add_ip = False
    add_user = False
    '''def get_obj(self, bl, pk, ppk): pass'''
    def get_redirection(self, user, model):
        return reverse(
            self.on_success,
            None,
            self.on_success_args,
            self.on_success_kwargs
        )
    def build_form(self, bl=None, req_data=None, pk='0', ppk='0'):
        obj = self.get_obj(bl,pk,ppk)
        if self.add_ip:
            obj.ip = bl._ip
        if self.add_user:
            obj.user = bl.user
        return self.form(req_data,instance=obj)
    def get(self,request,pk='0', ppk='0'):
        rd = request.GET
        if len(rd) == 0:
            rd = None
        return render(request,self.template_name,{
            'title': self.pagetitle,
            'form': self.build_form(ctrl.BusinessLogic(request), rd, pk, ppk),
        })
    def post(self,request,pk='0', ppk='0'):
        bl = ctrl.BusinessLogic(request)
        form = self.build_form(bl,request.POST, pk, ppk)
        err = ''
        saved = False
        try:
            if form.is_valid():
                form.save()
                saved = True
                return HttpResponseRedirect(self.get_redirection(bl.user, form.instance))
        except Exception as e:
            err = escape(str(e)).strip().replace('\n','\n<br>\n')
        return render(request, self.template_name,{
            'title': self.pagetitle,
            'form': form,
            'err': err,
        })

class CrudListView(TemplateViewLoggedIn):
    '''    Displays ForeingKey fields - such as lists    '''
    pagetitle = '???'
    template_name = "forms/crudlist.html"
    '''
    pagetitle = '???'
    template_name = "forms/crudlist.html"
    item_template = None
    edit_url_label = None
    delete_url_label = None
    def get_list_items(self, bl, ppk): pass
    '''
    def get(self,request,ppk='0'):
        items = self.get_list_items(ctrl.BusinessLogic(request), ppk)
        ll = ['0']
        if ppk!='0': ll=[ppk,'0']
        return render(request,self.template_name,{
            'title': self.pagetitle,
            'items': items,
            'current_pk': ppk,
            'item_template': self.item_template,
            'addlink': reverse(self.edit_url_label,None,ll),
            'delete_url_label': self.delete_url_label,
            'edit_url_label': self.edit_url_label,
        })

class CrudDeleteView(TemplateViewLoggedIn):
    '''    Deletes ForeingKey fields - such as list items    '''
    pagetitle = '???'
    '''
    pagetitle = '???'
    def get_redirection(self, user, model): pass
    def get_model(self, bl, pk): pass
    '''
    def get(self,request,pk='0'):
        bl = ctrl.BusinessLogic(request)
        redir = self.get_redirection(bl.user, None)
        if pk!='0':
            model = self.get_model(bl,pk)
            redir = self.get_redirection(bl.user, model)
            model.delete()
        return HttpResponseRedirect(redir)

class CrudEditView(UserPartEditFormView):
    '''    Edits/adds ForeingKey fields - such as list items    '''
    pagetitle = '???'
    template_name = "forms/form.html"
    on_success = None
    add_ip = True
    add_user = True
    manager = None
    def get_obj(self, bl, pk, ppk):
        if pk=='0':
            obj = self.manager()
            if ppk!='0':
                self.insert_parent(obj, bl, ppk)
            return obj
        else: return self.manager.objects.get(pk=pk, user__pk=bl.user.pk)

#
# CONCRETE VIEWS
#

class HomeView(TemplateView):
    template_name = "index.html"
    def get(self,request):
        bl = ctrl.BusinessLogic(request)
        d = {}
        d['bl'] = bl
        d['loginform'] = False
        if not bl.logged_in:
            d['loginform'] = forms.AuthenticationForm()
        else:
            d['corpora'] = ctrl.models.Corpus.objects.filter(user__id=bl.user.id)
            d['corpora'] = sorted(d['corpora'], key=lambda a: a.modifiedWithChild)[::-1]
        return render(
            request,
            self.template_name,
            d
        )

class SettingsView(TemplateViewLoggedIn):
    template_name = "settings/index.html"

class CorpusView(CrudListView):
    template_name = "corpus/view.html"
    pagetitle = 'Corpus'
    item_template = 'forms/listitem_corpus_document.html'
    edit_url_label = 'document_edt'
    delete_url_label = 'document_del'
    def get_list_items(self, bl, ppk): return ctrl.models.Document.objects.filter(corpus__pk=ppk, user__pk=bl.user.pk).order_by('title')

class CorpusDelView(CrudDeleteView):
    def get_model(self, bl, pk): return ctrl.models.Corpus.objects.get(pk=pk, user__pk=bl.user.pk)
    def get_redirection(self, user, model): return reverse('index')

class CorpusEdtView(CrudEditView):
    template_name = "corpus/form.html"
    pagetitle = 'Corpus'
    on_success = 'index'
    form = forms.CorpusForm
    manager = ctrl.models.Corpus

class CorpusXplView(TemplateView):
    def post(self,request,pk='0', ppk='0'):
        return self.get(request,pk,ppk)
    def get(self,request,pk='0', ppk='0'):
        return HttpResponseRedirect(reverse('analysis', None, [pk]))

class DocumentDelView(CrudDeleteView):
    def get_model(self, bl, pk): return ctrl.models.Document.objects.get(pk=pk, user__pk=bl.user.pk)
    def get_redirection(self, user, model):
        if model is None: return reverse('index')
        else: return reverse('corpus', None, [model.corpus.pk])

class DocumentEdtView(CrudEditView):
    template_name = 'corpus/docform.html'
    pagetitle = 'Document'
    on_success = 'corpus'
    form = forms.DocumentForm
    manager = ctrl.models.Document
    def insert_parent(self, obj, bl, ppk):
        exc = ctrl.models.Corpus.objects.get(user__pk=bl.user.pk, pk=ppk)
        obj.corpus = exc
    def get_redirection(self, user, model):
        self.on_success_args = [model.corpus.pk]
        return super().get_redirection(user,model)

class AnalysisView(TemplateView):
    template_name = 'analysis.html'
    def get(self, request, pk='0'):
        return render(request, self.template_name, {
            'corpus_pk': pk,
            'tools': analysisOptions,
        })
