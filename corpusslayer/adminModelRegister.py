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

from django.db import models
from corpusslayer.stackOverflowSnippets import classesInModule

def onlyModels(userMadeModels):
    return [ model for model in userMadeModels if models.Model in model.__mro__ ]

def isAbstract(clazz):
    try:
        return clazz.Meta.abstract
    except:
        return False

def discardAbstractModels(userMadeModels):
    return [ model for model in userMadeModels if not isAbstract(model) ]

def registrableModelsInModule(module):
    return discardAbstractModels(onlyModels(classesInModule(module)))

from django.core import exceptions
from sys import stderr

def registerForMe(admin, models_module):
    for model in registrableModelsInModule(models_module):
        try:
            admin.site.register(model)
        except exceptions.ImproperlyConfigured:
            pass
        except Exception as e:
            print(str(e.__class__)+': '+str(e) ,file=stderr)
