#    Copyright 2021 Mail.ru Group.
#
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

import unittest
import webob

from restalchemy.api import applications
from restalchemy.tests.functional.restapi.ra_based.microservice import routes


class WSGITestApp(applications.WSGIApp):

    def process_request(self, req):
        return req.__class__.__name__


class MyRequest(webob.Request):
    test_attr = 'yes'


class ApplicationsTestCase(unittest.TestCase):
    def setUp(self):
        self.req = webob.Request.blank('/some-uri')
        return super(ApplicationsTestCase, self).setUp()

    # def test_default_app(self):
    #     app = WSGITestApp(routes.Root)

    #     response = app(self.req)
    #     self.assertEqual(response, 'success')

    # def test_app_with_custom_request_class(self):
    #     app = WSGITestApp(routes.Root, request_class=MyRequest)

    #     response = app({'env_emulate': True}, 'utf8')
    #     raise Exception
    #     self.assertEqual(response, 'success')
