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

from django import template
register = template.Library()

import base64
import json
import urllib.parse

@register.filter
def tobase64(value):
    if not isinstance(value, bytes):
        value = value.encode('utf-8')
    return base64.b64encode(value)

@register.filter
def tojson(value):
    return json.dumps(value)

@register.filter
def tojsonb64(value):
    return tobase64(tojson(value))

@register.filter
def tourlquoted(value):
    return urllib.parse.quote_plus(value)

@register.filter
def tourlparams(value):
    return urllib.parse.urlencode(value)

@register.filter
def todict(value):
    return dict(value)

@register.filter
def tolist(value):
    return list(value)

@register.filter
def dictitems(value):
    return value.items()

@register.filter
def applyzip(value):
    return zip(value)

@register.filter
def toint(value):
    return int(value)

@register.filter
def tofloat(value):
    return float(value)
