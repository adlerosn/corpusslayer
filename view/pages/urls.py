"""corpusslayer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls import include
from view.pages import views
import registration.backends.default.urls as registration_urls
import server_secrets.pluginUrls as plugin_urls

urlpatterns = [
    url(r'^accounts/', include(registration_urls)),
    url(r'^$', views.HomeView.as_view(), name='index'),
    url(r'^settings/?$', views.SettingsView.as_view(), name='my_account'),

    url(r'^legal/priv/?$', views.LegalPrivView.as_view(), name='privacy'),
    url(r'^legal/tos/?$', views.LegalTosView.as_view(), name='tos'),
    url(r'^help/?$', views.HelpView.as_view(), name='help'),

    url(r'^corpus/(?P<ppk>[0-9]+)/?$', views.CorpusView.as_view(), name='corpus'),
    url(r'^corpus/(?P<pk>[0-9]+)/edt/?$', views.CorpusEdtView.as_view(), name='corpus_edt'),
    url(r'^corpus/(?P<pk>[0-9]+)/del/?$', views.CorpusDelView.as_view(), name='corpus_del'),
    url(r'^corpus/(?P<pk>[0-9]+)/xpl/?$', views.CorpusXplView.as_view(), name='corpus_xpl'),

    url(r'^document/(?P<pk>[0-9]+)/edt/?$', views.DocumentEdtView.as_view(), name='document_edt'),
    url(r'^document/(?P<ppk>[0-9]+)-(?P<pk>[0-9]+)/edt/?$', views.DocumentEdtView.as_view(), name='document_edt'),
    url(r'^document/(?P<pk>[0-9]+)/del/?$', views.DocumentDelView.as_view(), name='document_del'),
    url(r'^document/(?P<ppk>[0-9]+)-(?P<pk>[0-9]+)/del/?$', views.DocumentDelView.as_view(), name='document_del'),

    url(r'^server-stats$', views.ServerStatsView.as_view(), name='server_stats'),
    #url(r'^server-stats\.json$', views.ServerStatsJsonGetter, name='server_stats_json'),

    url(r'^analysis\.(?P<pk>[0-9]+)$', views.AnalysisView.as_view(), name='analysis'),
    url(r'^analysis\.(?P<corpus_pk>[0-9]+)/', include(plugin_urls)),
]
