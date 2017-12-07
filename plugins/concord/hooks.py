import os
pluginName = os.path.abspath(__file__).split(os.path.sep)[-2]
pluginNameFriendly = (pluginName[0].upper()+pluginName[1:]).replace('_',' ')
from corpusslayer.hooks import getAnalysisOptionsEmptyContainer
from corpusslayer.bootstrap_constants import COLOR
from django.utils.translation import ugettext_lazy as _

randomfactor = .125468

def getAnalysisOptions():
    option = getAnalysisOptionsEmptyContainer(
        pluginName = pluginName,
    )
    option['text'] = _('Concordancer [concord]')
    option['icon'] = 'th'
    option['priority'] = 500+randomfactor
    return [option]

def getHooks(): #-> dict[String,list[Callable]]
    return {}
