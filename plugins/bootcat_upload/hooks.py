import os
pluginName = os.path.abspath(__file__).split(os.path.sep)[-2]
pluginNameFriendly = (pluginName[0].upper()+pluginName[1:]).replace('_',' ')
from corpusslayer.hooks import getAnalysisOptionsEmptyContainer
from corpusslayer.bootstrap_constants import COLOR
from django.utils.translation import ugettext_lazy as _

randfactor = .254698

def getAnalysisOptions():
    option = getAnalysisOptionsEmptyContainer(
        pluginName = pluginName,
    )
    option['text'] = _("Upload corpus built with BootCaT [bootcat_upload]")
    option['priority'] = -5000+randfactor
    option['color'] = COLOR.YELLOW
    option['icon'] = 'plus'
    return [option]
