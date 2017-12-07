from corpusslayer.bootstrap_constants import COLOR

def getAnalysisOptionsEmptyContainer(
    text = 'Template',
    pluginName = 'template'
    ):
    return {
        'priority': 100.,
        'icon': 'pencil',
        'text': text+' ['+pluginName+']',
        'plugin': pluginName,
        'color': COLOR.BLUE,
        'link': pluginName+'_index',
    }
