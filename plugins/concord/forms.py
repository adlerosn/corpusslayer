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
importline = 'import '+('.'.join(['plugins',pluginName,'models'])+' as models')
exec(importline) #import plugins.thisplugin.models as models

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from application import models as app_models
from application import forms as app_forms

class SearchForm(forms.Form):
    tagged_corpus = forms.ChoiceField(required=True, label=_('Tagged corpus'))
    neighborhood_visibility = forms.ChoiceField(required=False, label=_('Neighborhood visibility'),choices=[
        ('-1',_('Whole sentence')),
        ('6',_('6 tokens for each side')),
        ('5',_('5 tokens for each side')),
        ('4',_('4 tokens for each side')),
        ('3',_('3 tokens for each side')),
        ('2',_('2 tokens for each side')),
        ('1',_('1 token for each side')),
        ('0',_('Only the matched content')),
    ])
    query = forms.CharField(required=True, label=_('Query'))
