# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2018 Eugene Frolov <eugene@frolov.net.ru>
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

from restalchemy.storage.sql import filters
from restalchemy.tests.unit import base


TEST_NAME = 'FAKE_NAME'
TEST_VALUE = 'FAKE_VALUE'


class EQTestCase(base.BaseTestCase):

    def setUp(self):
        self._expr = filters.EQ(value=TEST_VALUE)

    def test_construct_expression(self):

        result = self._expr.construct_expression(name=TEST_NAME)

        self.assertEqual(result, '`' + TEST_NAME + '` = %s')

    def test_value_property(self):
        self.assertEqual(self._expr.value, TEST_VALUE)


class NETestCase(base.BaseTestCase):

    def setUp(self):
        self._expr = filters.NE(value=TEST_VALUE)

    def test_construct_expression(self):

        result = self._expr.construct_expression(name=TEST_NAME)

        self.assertEqual(result, '`' + TEST_NAME + '` <> %s')

    def test_value_property(self):
        self.assertEqual(self._expr.value, TEST_VALUE)


class GTTestCase(base.BaseTestCase):

    def setUp(self):
        self._expr = filters.GT(value=TEST_VALUE)

    def test_construct_expression(self):

        result = self._expr.construct_expression(name=TEST_NAME)

        self.assertEqual(result, '`' + TEST_NAME + '` > %s')

    def test_value_property(self):
        self.assertEqual(self._expr.value, TEST_VALUE)


class GETestCase(base.BaseTestCase):

    def setUp(self):
        self._expr = filters.GE(value=TEST_VALUE)

    def test_construct_expression(self):

        result = self._expr.construct_expression(name=TEST_NAME)

        self.assertEqual(result, '`' + TEST_NAME + '` >= %s')

    def test_value_property(self):
        self.assertEqual(self._expr.value, TEST_VALUE)


class LTTestCase(base.BaseTestCase):

    def setUp(self):
        self._expr = filters.LT(value=TEST_VALUE)

    def test_construct_expression(self):

        result = self._expr.construct_expression(name=TEST_NAME)

        self.assertEqual(result, '`' + TEST_NAME + '` < %s')

    def test_value_property(self):
        self.assertEqual(self._expr.value, TEST_VALUE)


class LETestCase(base.BaseTestCase):

    def setUp(self):
        self._expr = filters.LE(value=TEST_VALUE)

    def test_construct_expression(self):

        result = self._expr.construct_expression(name=TEST_NAME)

        self.assertEqual(result, '`' + TEST_NAME + '` <= %s')

    def test_value_property(self):
        self.assertEqual(self._expr.value, TEST_VALUE)


class IsTestCase(base.BaseTestCase):

    def setUp(self):
        self._expr = filters.Is(value=TEST_VALUE)

    def test_construct_expression(self):

        result = self._expr.construct_expression(name=TEST_NAME)

        self.assertEqual(result, '`' + TEST_NAME + '` IS %s')

    def test_value_property(self):
        self.assertEqual(self._expr.value, TEST_VALUE)


class IsNotTestCase(base.BaseTestCase):

    def setUp(self):
        self._expr = filters.IsNot(value=TEST_VALUE)

    def test_construct_expression(self):

        result = self._expr.construct_expression(name=TEST_NAME)

        self.assertEqual(result, '`' + TEST_NAME + '` IS NOT %s')

    def test_value_property(self):
        self.assertEqual(self._expr.value, TEST_VALUE)
