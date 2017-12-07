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
from django.contrib import admin
from django.views.generic import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage
import django.conf.urls.i18n
import view.pages as pages
import view.pages.urls as pages_urls
import view.api.urls as api_urls
import rosetta.urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(api_urls)),
    url(r'^favicon\.ico$', RedirectView.as_view(url=staticfiles_storage.url('favicon.ico'), permanent=False), name="favicon"),
    url(r'^', include(pages_urls)),
    url(r'^rosetta/', include(rosetta.urls)),
    url(r'^i18n/', include(django.conf.urls.i18n)),
]

#urlpatterns += django.conf.urls.i18n.i18n_patterns(
#    #url(r'^$',pages.views.SoonView.as_view()),
#    prefix_default_language=True
#)
