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

import contextlib
import logging


class MySQLSession(object):

    def __init__(self, conn):
        self._conn = conn
        self._cursor = conn.cursor(dictionary=True)
        self._log = logging.getLogger(__name__)

    def execute(self, statement, values):
        self._log.debug("Execute statement %s with values %s",
                        statement, values)
        self._cursor.execute(statement, values)
        return self._cursor

    def rollback(self):
        self._conn.rollback()

    def commit(self):
        self._conn.commit()

    def close(self):
        self._conn.close()


@contextlib.contextmanager
def session_manager(engine, session=None):
    if session is None:
        session = engine.get_session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
    else:
        yield session
