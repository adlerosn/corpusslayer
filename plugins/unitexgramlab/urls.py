import os
pluginName = os.path.abspath(__file__).split(os.path.sep)[-2]
importline = 'import '+('.'.join(['plugins',pluginName,'views'])+' as views')
exec(importline) #import plugins.thisplugin.views as views

from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.SoonView.as_view(), name=pluginName+'_index'),
    url(r'^nuke/?$', views.NukeView.as_view(), name=pluginName+'_nuke'),
    url(r'^process/?$', views.ProcessView.as_view(), name=pluginName+'_process'),
    url(r'^wait/(?P<job_pk>[0-9]+)/?$', views.JobWaiterView.as_view(), name=pluginName+'_job_wait'),
    url(r'^sentences/?$', views.SentenceListView.as_view(), name=pluginName+'_sentences'),
    url(r'^wordfreq/?$', views.WordFreqView.as_view(), name=pluginName+'_wordfreq'),
    url(r'^wordlist/?$', views.WordListView.as_view(), name=pluginName+'_wordlist'),
    url(r'^sntauto/?$', views.SentenceAutomatonView.as_view(), name=pluginName+'_sntauto'),
    url(r'^txtauto\.html$', views.TextAutomatonView.as_view(), name=pluginName+'_txtauto'),
    url(r'^txtauto\.(?P<fmt>\w+)$', views.TextAutomatonDownload.as_view(), name=pluginName+'_txtauto_dwn'),
    url(r'^txtauto/missing$', views.TextAutomatonMissingView.as_view(), name=pluginName+'_txtauto_missing'),
]
