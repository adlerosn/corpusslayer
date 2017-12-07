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
from django.db import models
import application.models as app_models

# Create your models here.

class CorpusMxterminated(app_models.DiscardsIP):
    corpus = models.OneToOneField(app_models.Corpus, unique=True, on_delete=models.CASCADE, null=True, blank=True, related_name=pluginName+'_snt_cache')
    user = models.ForeignKey(app_models.User, on_delete=models.CASCADE, null=False, blank=False)
    sentences = models.TextField(null=True, blank=True)
    def __str__(self):
        return str(self.corpus)+', by '+str(self.user)+' - cached as pk #'+str(self.pk)

class CorpusMxposted(app_models.DiscardsIP):
    corpus = models.OneToOneField(app_models.Corpus, unique=True, on_delete=models.CASCADE, null=True, blank=True, related_name=pluginName+'_tag_cache')
    user = models.ForeignKey(app_models.User, on_delete=models.CASCADE, null=False, blank=False)
    postags = models.TextField(null=True, blank=True)
    def __str__(self):
        return str(self.corpus)+', by '+str(self.user)+' - cached as pk #'+str(self.pk)
