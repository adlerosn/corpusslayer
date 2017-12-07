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

from django.contrib.auth.context_processors import auth
from django.contrib.auth import logout
from django.utils.timezone import now
from application import models

def getIpFromRequest(rq):
    ipaddress = ''
    x_forwarded_for = rq.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ipaddress = x_forwarded_for.split(',')[-1].strip()
    else:
        ipaddress = rq.META.get('REMOTE_ADDR')
    return ipaddress

class BusinessException(Exception): pass
class SiteBannedException(BusinessException): pass

class Business(object):
    _request = None
    _ip = None
    _user = None
    def __init__(self, request):
        self._request = request
        self._ip = getIpFromRequest(request)
        user = auth(request)['user']
        bans = (
            models.
            SiteBan.
            objects.
            filter(active=True).
            filter(user_id=user.id).
            order_by('-lastRevision')
        )
        if len(bans) > 0:
            logout(request)
            raise SiteBannedException(
                bans[0].
                notes
            )
        self._user = user
    @property
    def user(self):
        return self._user
