# Copyright (c) 2017 Adler Neves <adlerosn@gmail.com>
#
# MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from secrets.hookModules import hookModules

class HookOption:
    def __init__(self, module, handler):
        self.module = module
        self.handler = handler

hookOptions = dict()
for module in hookModules:
    if hasattr(module, 'getHooks'):
        hooks = module.getHooks()
        if isinstance(hooks, dict):
            for event, callbacks in hooks.items():
                if isinstance(event, str) and isinstance(callbacks, list):
                    if event not in hookOptions:
                        hookOptions[event] = list()
                    hookOptions[event]+=map(lambda c: HookOption(module,c), callbacks)

del hookModules

def fire(event, data=None):
    '''
    event: str = the event fired
    data: object? = auxiliary data for the desired event
    ---
    Event types:

    filter -> data should be a collection
    the use case is either removing data from user sight, sorting or transforming it somehow
    it usually is the last stage before data goes to the user
    example: one stage of "filter:sentencelist" can replace all curse words by asterisks

    action -> data can be anything
    the usecase is when you finish doing something and wants to notify something happened
    example: "action:xyz_tool:preprocessing:result"
    example: "action:sentencelist:result"

    query -> data can be anything
    the use case is when data related to the one provided needs to be taken out of other plugins
    example: "query:sentencelist" (where data is the corpus, and the return is a list of dicts, where one entry contains the callback to the plugins that provides such feature)

    provider -> data will remain unused
    the use case is when one plugin can have its features extended by
    example: "provider:xyz_tool" (an "jkl_dataset" can provide assets for the "xyz_tool" plugin)

    ---

    Quick review:

    provider -> none Input, list Output
    query    -> any  Input, list Output
    filter   -> iter Input, iter Output
    action   -> any  Input, none Output

    ---

    This part of the platform gives you no guarantee that some recursion loop won't
    happen when more than one plugin acts; because of that, avoid breaking the
    sequence:
            provider -> query -> filter -> action
    No problem in skipping some stage; but can be some problem in firing the previous
    stages on a further stage. Also, avoid firing events on the same stage of a
    fired event.
    '''
    if not isinstance(event,str):
        raise TypeError("Event should be a string")
    elif ':' not in event:
        raise NameError('All events should have a prefix. Ex: "query:provider:sentencelist"')
    elif event.startswith('filter:'):
        if not hasattr(data,'__iter__'):
            raise AttributeError('data provided should be iterable')
        for hookOption in hookOptions.get(event,list()):
            data = hookOption.handler(data)
        return data
    elif event.startswith('action:'):
        for hookOption in hookOptions.get(event,list()):
            hookOption.handler(data)
        return
    elif event.startswith('query:'):
        result = list()
        for hookOption in hookOptions.get(event,list()):
            result.append(hookOption.handler(data))
        return result
    elif event.startswith('provider:'):
        result = list()
        for hookOption in hookOptions.get(event,list()):
            result.append(hookOption.handler())
        return result
    else:
        raise NotImplementedError('Event wasn\'t implented: '+str(event))

from urllib.parse import quote as urlGet

def buildNextGetPart(url):
    return '?next='+urlGet(url, safe='')

def nextGetArg(redirect, url):
    redirect['Location']+=buildNextGetPart(url)
    return redirect
