import os
pluginName = os.path.abspath(__file__).split(os.path.sep)[-2]
importline = 'import '+('.'.join(['plugins',pluginName,'models'])+' as models')
exec(importline) #import plugins.thisplugin.models as models
from corpusslayer.adminModelRegister import registerForMe
from django.contrib import admin

# Register your models here.

registerForMe(admin, models)
