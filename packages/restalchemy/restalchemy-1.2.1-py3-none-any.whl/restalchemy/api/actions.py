# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2014 Eugene Frolov <eugene@frolov.net.ru>
#
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from restalchemy.common import exceptions as exc


class ActionHandler(object):

    def __init__(self, get=None, post=None, put=None):
        self._get = get
        self._post = post
        self._put = put

    def get(self, fn):
        self._get = fn
        return self

    def post(self, fn):
        self._post = fn
        return self

    def put(self, fn):
        self._put = fn
        return self

    def do(self, fn, controller, *args, **kwargs):
        if fn:
            result = fn(self=controller, *args, **kwargs)
            return controller.process_result(result)
        else:
            raise exc.NotImplementedError()

    def do_get(self, *args, **kwargs):
        return self.do(self._get, *args, **kwargs)

    def do_post(self, *args, **kwargs):
        return self.do(self._post, *args, **kwargs)

    def do_put(self, *args, **kwargs):
        return self.do(self._put, *args, **kwargs)


def get(fn):
    return ActionHandler(get=fn)


def post(fn):
    return ActionHandler(post=fn)


def put(fn):
    return ActionHandler(put=fn)
