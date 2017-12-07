import os
pluginName = os.path.abspath(__file__).split(os.path.sep)[-2]
importline = 'import '+('.'.join(['plugins',pluginName,'views'])+' as views')
exec(importline) #import plugins.thisplugin.views as views

from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.SoonView.as_view(), name=pluginName+'_index'),
    url(r'^license/?$', views.LicenseView.as_view(), name=pluginName+'_license'),
    url(r'^sentences/?$', views.TermSentencesView.as_view(), name=pluginName+'_sentences'),
    url(r'^sentences/process/?$', views.TermProcessView.as_view(), name=pluginName+'_sentences_process'),
    url(r'^sentences/nuke/?$', views.TermNukeView.as_view(), name=pluginName+'_sentences_nuke'),
    url(r'^tags/?$', views.PostTagView.as_view(), name=pluginName+'_tags'),
    url(r'^tags/process/?$', views.PostTagProcessView.as_view(), name=pluginName+'_tags_process'),
    url(r'^tags/nuke/?$', views.PostTagNukeView.as_view(), name=pluginName+'_tags_nuke'),
]
