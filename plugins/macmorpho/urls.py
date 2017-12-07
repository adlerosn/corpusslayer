import os
pluginName = os.path.abspath(__file__).split(os.path.sep)[-2]
importline = 'import '+('.'.join(['plugins',pluginName,'views'])+' as views')
exec(importline) #import plugins.thisplugin.views as views

from django.conf.urls import url

urlpatterns = [
    url(r'^', views.SoonView.as_view(), name=pluginName+'_index'),
]
