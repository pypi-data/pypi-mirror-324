# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2017 Eugene Frolov <eugene@frolov.net.ru>
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

from restalchemy.storage.sql.dialect import mysql
from restalchemy.storage.sql import filters
from restalchemy.tests.unit import base


class FakeTable(object):

    name = 'FAKE_TABLE'

    def get_column_names(self, with_pk=True, do_sort=True):
        if with_pk:
            return ["pk", "field_int", "field_str", "field_bool"]
        return ["field_int", "field_str", "field_bool"]

    def get_escaped_column_names(self, with_pk=True, do_sort=True):
        if with_pk:
            return ["`pk`", "`field_int`", "`field_str`", "`field_bool`"]
        return ["`field_int`", "`field_str`", "`field_bool`"]

    def get_pk_names(self, do_sort=True):
        return ["pk"]

    def get_escaped_pk_names(self, do_sort=True):
        return ["`pk`"]


FAKE_VALUES = ["pk", 111, "field2", True]
FAKE_PK_VALUES = ["pk"]


class MySQLInsertTestCase(base.BaseTestCase):

    def setUp(self):
        self.target = mysql.MySQLInsert(FakeTable(), FAKE_VALUES)

    def test_statement(self):
        self.assertEqual(
            self.target.get_statement(),
            "INSERT INTO `FAKE_TABLE` (`pk`, `field_int`, `field_str`, "
            "`field_bool`) VALUES (%s, %s, %s, %s)")


class MySQLUpdateTestCase(base.BaseTestCase):

    def setUp(self):
        TABLE = FakeTable()
        self.target = mysql.MySQLUpdate(TABLE, FAKE_PK_VALUES,
                                        FAKE_VALUES)

    def test_statement(self):
        self.assertEqual(
            self.target.get_statement(),
            "UPDATE `FAKE_TABLE` SET `field_int` = %s, `field_str` = %s, "
            "`field_bool` = %s WHERE `pk` = %s")


class MySQLDeleteTestCase(base.BaseTestCase):

    def setUp(self):
        TABLE = FakeTable()

        self.target = mysql.MySQLDelete(TABLE, FAKE_PK_VALUES)

    def test_statement(self):
        self.assertEqual(
            self.target.get_statement(),
            "DELETE FROM `FAKE_TABLE` WHERE `pk` = %s")


class MySQLSelectTestCase(base.BaseTestCase):

    def setUp(self):
        self._TABLE = FakeTable()

    def test_statement(self):
        target = mysql.MySQLSelect(self._TABLE, dict(zip(
            self._TABLE.get_column_names(), FAKE_VALUES)))

        result = target.get_statement()

        self.assertEqual(
            result,
            "SELECT `pk`, `field_int`, `field_str`, `field_bool` "
            "FROM `FAKE_TABLE` WHERE `field_bool` = %s AND "
            "`field_int` = %s AND `field_str` = %s AND `pk` = %s")

    def test_statement_EQ(self):
        FAKE_EQ_VALUES = [filters.EQ(v) for v in FAKE_VALUES]
        target = mysql.MySQLSelect(self._TABLE, dict(zip(
            self._TABLE.get_column_names(), FAKE_EQ_VALUES)))

        result = target.get_statement()

        self.assertEqual(
            result,
            "SELECT `pk`, `field_int`, `field_str`, `field_bool` "
            "FROM `FAKE_TABLE` WHERE `field_bool` = %s AND "
            "`field_int` = %s AND `field_str` = %s AND `pk` = %s")

    def test_statement_NE(self):
        FAKE_NE_VALUES = [filters.NE(v) for v in FAKE_VALUES]
        target = mysql.MySQLSelect(self._TABLE, dict(zip(
            self._TABLE.get_column_names(), FAKE_NE_VALUES)))

        result = target.get_statement()

        self.assertEqual(
            result,
            "SELECT `pk`, `field_int`, `field_str`, `field_bool` "
            "FROM `FAKE_TABLE` WHERE `field_bool` <> %s AND "
            "`field_int` <> %s AND `field_str` <> %s AND `pk` <> %s")

    def test_statement_GT(self):
        FAKE_GT_VALUES = [filters.GT(v) for v in FAKE_VALUES]
        target = mysql.MySQLSelect(self._TABLE, dict(zip(
            self._TABLE.get_column_names(), FAKE_GT_VALUES)))

        result = target.get_statement()

        self.assertEqual(
            result,
            "SELECT `pk`, `field_int`, `field_str`, `field_bool` "
            "FROM `FAKE_TABLE` WHERE `field_bool` > %s AND "
            "`field_int` > %s AND `field_str` > %s AND `pk` > %s")

    def test_statement_GE(self):
        FAKE_GE_VALUES = [filters.GE(v) for v in FAKE_VALUES]
        target = mysql.MySQLSelect(self._TABLE, dict(zip(
            self._TABLE.get_column_names(), FAKE_GE_VALUES)))

        result = target.get_statement()

        self.assertEqual(
            result,
            "SELECT `pk`, `field_int`, `field_str`, `field_bool` "
            "FROM `FAKE_TABLE` WHERE `field_bool` >= %s AND "
            "`field_int` >= %s AND `field_str` >= %s AND `pk` >= %s")

    def test_statement_LT(self):
        FAKE_LT_VALUES = [filters.LT(v) for v in FAKE_VALUES]
        target = mysql.MySQLSelect(self._TABLE, dict(zip(
            self._TABLE.get_column_names(), FAKE_LT_VALUES)))

        result = target.get_statement()

        self.assertEqual(
            result,
            "SELECT `pk`, `field_int`, `field_str`, `field_bool` "
            "FROM `FAKE_TABLE` WHERE `field_bool` < %s AND "
            "`field_int` < %s AND `field_str` < %s AND `pk` < %s")

    def test_statement_LE(self):
        FAKE_LE_VALUES = [filters.LE(v) for v in FAKE_VALUES]
        target = mysql.MySQLSelect(self._TABLE, dict(zip(
            self._TABLE.get_column_names(), FAKE_LE_VALUES)))

        result = target.get_statement()

        self.assertEqual(
            result,
            "SELECT `pk`, `field_int`, `field_str`, `field_bool` "
            "FROM `FAKE_TABLE` WHERE `field_bool` <= %s AND "
            "`field_int` <= %s AND `field_str` <= %s AND `pk` <= %s")
