# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2016 Eugene Frolov <eugene@frolov.net.ru>
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

import random

import mock
import requests
from six.moves.urllib import parse
from sqlalchemy.orm import exc

from restalchemy.common import utils
from restalchemy.tests.functional.restapi.sa_based.microservice import db
from restalchemy.tests.functional.restapi.sa_based.microservice import models
from restalchemy.tests.functional.restapi.sa_based.microservice import service
from restalchemy.tests.unit import base


TEMPL_SERVICE_ENDPOINT = utils.lastslash("http://127.0.0.1:%s/")
TEMPL_ROOT_COLLECTION_ENDPOINT = TEMPL_SERVICE_ENDPOINT
TEMPL_V1_COLLECTION_ENDPOINT = utils.lastslash(parse.urljoin(
    TEMPL_SERVICE_ENDPOINT, 'v1'))
TEMPL_VMS_COLLECTION_ENDPOINT = utils.lastslash(parse.urljoin(
    TEMPL_V1_COLLECTION_ENDPOINT, 'vms'))
TEMPL_VM_RESOURCE_ENDPOINT = parse.urljoin(TEMPL_VMS_COLLECTION_ENDPOINT, '%s')
TEMPL_POWERON_ACTION_ENDPOINT = parse.urljoin(
    utils.lastslash(TEMPL_VM_RESOURCE_ENDPOINT),
    'actions/poweron/invoke')


class BaseResourceTestCase(base.BaseTestCase):

    def get_endpoint(self, template, *args):
        return template % ((self.service_port,) + tuple(args))

    def setUp(self):
        super(BaseResourceTestCase, self).setUp()
        self.service_port = random.choice(range(2100, 2200))
        url = parse.urlparse(self.get_endpoint(TEMPL_SERVICE_ENDPOINT))
        self._service = service.RESTService(bind_host=url.hostname,
                                            bind_port=url.port)
        self._service.start()

    def tearDown(self):
        super(BaseResourceTestCase, self).tearDown()
        self._service.stop()


class TestRootResourceTestCase(BaseResourceTestCase):

    def test_get_versions_list(self):

        response = requests.get(self.get_endpoint(
            TEMPL_ROOT_COLLECTION_ENDPOINT))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), ["v1"])


class TestVersionsResourceTestCase(BaseResourceTestCase):

    def test_get_resources_list(self):

        response = requests.get(
            self.get_endpoint(TEMPL_V1_COLLECTION_ENDPOINT))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), ["vms"])


class TestVMResourceTestCase(BaseResourceTestCase):

    def _insert_vm_to_db(self, uuid, name, state):
        session_maker = db.get_session()
        session = session_maker()
        vm = models.VM(name=name, state=state)
        vm.uuid = uuid
        session.add(vm)
        session.commit()

    def _vm_exists_in_db(self, uuid):
        session_maker = db.get_session()
        session = session_maker()
        try:
            session.query(models.VM).filter(models.VM.uuid == uuid).one()
            return True
        except exc.NoResultFound:
            return False

    @mock.patch('uuid.uuid4')
    def test_create_vm_resource_successful(self, uuid4_mock):
        RESOURCE_ID = "00000000-0000-0000-0000-000000000001"
        uuid4_mock.return_value = RESOURCE_ID
        vm_request_body = {
            "name": "test"
        }
        vm_response_body = {
            "uuid": RESOURCE_ID,
            "name": "test",
            "state": "off"
        }
        LOCATION = self.get_endpoint(TEMPL_VM_RESOURCE_ENDPOINT, RESOURCE_ID)

        response = requests.post(self.get_endpoint(
            TEMPL_VMS_COLLECTION_ENDPOINT), json=vm_request_body)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.headers['location'], LOCATION)
        self.assertEqual(response.json(), vm_response_body)

    def test_get_vm_resource_by_uuid_successful(self):
        RESOURCE_ID = "00000000-0000-0000-0000-000000000001"
        self._insert_vm_to_db(uuid=RESOURCE_ID, name="test", state="off")
        vm_response_body = {
            "uuid": RESOURCE_ID,
            "name": "test",
            "state": "off"
        }
        VM_RES_ENDPOINT = self.get_endpoint(TEMPL_VM_RESOURCE_ENDPOINT,
                                            RESOURCE_ID)

        response = requests.get(VM_RES_ENDPOINT)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), vm_response_body)

    def test_update_vm_resource_successful(self):
        RESOURCE_ID = "00000000-0000-0000-0000-000000000001"
        self._insert_vm_to_db(uuid=RESOURCE_ID, name="old", state="off")
        vm_request_body = {
            "name": "new"
        }
        vm_response_body = {
            "uuid": RESOURCE_ID,
            "name": "new",
            "state": "off"
        }
        VM_RES_ENDPOINT = self.get_endpoint(TEMPL_VM_RESOURCE_ENDPOINT,
                                            RESOURCE_ID)

        response = requests.put(VM_RES_ENDPOINT, json=vm_request_body)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), vm_response_body)

    def test_delete_vm_resource_successful(self):
        RESOURCE_ID = "00000000-0000-0000-0000-000000000001"
        self._insert_vm_to_db(uuid=RESOURCE_ID, name="test", state="off")

        VM_RES_ENDPOINT = self.get_endpoint(TEMPL_VM_RESOURCE_ENDPOINT,
                                            RESOURCE_ID)

        response = requests.delete(VM_RES_ENDPOINT)

        self.assertEqual(response.status_code, 204)
        self.assertFalse(self._vm_exists_in_db(RESOURCE_ID))

    def test_process_vm_action_successful(self):
        RESOURCE_ID = "00000000-0000-0000-0000-000000000001"
        self._insert_vm_to_db(uuid=RESOURCE_ID, name="test", state="off")
        vm_response_body = {
            "uuid": RESOURCE_ID,
            "name": "test",
            "state": "on"
        }
        POWERON_ACT_ENDPOINT = self.get_endpoint(TEMPL_POWERON_ACTION_ENDPOINT,
                                                 RESOURCE_ID)

        response = requests.post(POWERON_ACT_ENDPOINT)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), vm_response_body)

    def test_get_collection_vms_successful(self):
        RESOURCE_ID1 = "00000000-0000-0000-0000-000000000001"
        RESOURCE_ID2 = "00000000-0000-0000-0000-000000000002"
        self._insert_vm_to_db(uuid=RESOURCE_ID1, name="test1", state="off")
        self._insert_vm_to_db(uuid=RESOURCE_ID2, name="test2", state="on")
        vm_response_body = [{
            "uuid": RESOURCE_ID1,
            "name": "test1",
            "state": "off"
        }, {
            "uuid": RESOURCE_ID2,
            "name": "test2",
            "state": "on"
        }]

        response = requests.get(self.get_endpoint(
            TEMPL_VMS_COLLECTION_ENDPOINT))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), vm_response_body)
