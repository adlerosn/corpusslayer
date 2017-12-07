import os
pluginName = os.path.abspath(__file__).split(os.path.sep)[-2]
importline = 'import '+('.'.join(['plugins',pluginName,'models'])+' as models')
exec(importline) #import plugins.thisplugin.models as models

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from application import models as app_models
from application import forms as app_forms
