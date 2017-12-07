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

from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

class Timestampable(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class DiscardsIP(Timestampable):
    class Meta:
        abstract = True

class RequiresIP(Timestampable):
    ip = models.GenericIPAddressField(blank=False,null=False)
    class Meta:
        abstract = True

class SiteBan(RequiresIP):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, related_name='banned_by')
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='banned')
    lastRevision = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True, null=False)
    notes = models.TextField(default='', blank=True, null=False)
    def __str__(self):
        return self.user.username

class Corpus(RequiresIP):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, related_name='corpora')
    title = models.CharField(default='', null=False, blank=False, max_length = 255,verbose_name=_('title'))
    language = models.CharField(default='en-us', null=False, blank=True, max_length = 10, verbose_name=_('language'))
    comments = models.TextField(default='', null=False, blank=False,verbose_name=_('comments'))
    class Meta:
        verbose_name=_('Corpus')
    @property
    def mergedDocuments(self):
        return str.join('\n\n', map(lambda doc: doc.text, self.documents.all()))
    @property
    def modifiedWithChild(self):
        try:
            return max(self.modified,max(list(map(lambda doc: doc.modified, self.documents.all()))))
        except ValueError:
            return self.modified
    def __str__(self):
        return str(self.title)+' - #'+str(self.pk)

class Document(RequiresIP):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    corpus = models.ForeignKey(Corpus, on_delete=models.CASCADE, null=False, blank=False, related_name='documents')
    title = models.CharField(default='', null=False, blank=False, max_length = 255, verbose_name=_('title'))
    source = models.CharField(default='', null=False, blank=False, max_length = 255, verbose_name=_('source'))
    text = models.TextField(default='', null=False, blank=True, verbose_name=_('text'))
    class Meta:
        verbose_name=_('Document')
    def __str__(self):
        return str(self.title)+' - #'+str(self.pk)

class Attribute(RequiresIP):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, related_name='tags_created')
    name = models.CharField(default='', null=False, blank=False, unique=True, max_length = 255)
    description = models.CharField(default='', null=False, blank=False, max_length = 255)
    help = models.TextField(default='', null=False, blank=False)
    def __str__(self):
        return str(self.name)+' - #'+str(self.pk)

class AttributeMixin(RequiresIP):
    class Meta:
        abstract = True
    value = models.TextField(default='', null=False, blank=False)

class DocumentAttribute(AttributeMixin):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, null=False, blank=False, related_name="attributes")
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, null=False, blank=False, related_name="documents")

class CorpusAttribute(AttributeMixin):
    document = models.ForeignKey(Corpus, on_delete=models.CASCADE, null=False, blank=False, related_name="attributes")
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, null=False, blank=False, related_name="corpora")

class Plugin(RequiresIP):
    enabled = models.BooleanField(default=False, null=False)
    codename = models.CharField(default='', null=False, blank=False, unique=True, max_length = 50)
    name = models.CharField(default='', null=False, blank=False, max_length = 255)
    description = models.TextField(default='', null=False, blank=False, max_length = 255)
    contact_name = models.CharField(default='', null=False, blank=False, max_length = 255)
    contact_email = models.CharField(default='', null=False, blank=False, max_length = 255)
    authors = models.TextField(default='', null=False, blank=False)
    license_name = models.CharField(default='', null=False, blank=False, max_length = 255)
    license_link = models.CharField(default='', null=False, blank=False, max_length = 255)
    copyright_line_text = models.TextField(default='', null=False, blank=True)
    copyright_line_link = models.TextField(default='', null=False, blank=True)
    update_url = models.CharField(default='', null=False, blank=False, max_length = 255)
    forbid_python2 = models.BooleanField(default=False, null=False)
    forbid_python3 = models.BooleanField(default=False, null=False)
    version_label = models.CharField(default='1.0.0', null=False, blank=False, max_length = 15)
    version_timestamp = models.DateTimeField(default=now, null=False, blank=False)
    requirements_check_script = models.TextField(default='', null=False, blank=False)
