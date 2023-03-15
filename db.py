import sqlite3
import os.path
from datetime import datetime, timezone
import sys
from util import s_quote

def check_table(cur, table_name, columns):
    try:
        cur.execute("SELECT %s FROM %s WHERE 1=2" % (', '.join(columns), table_name))
        return True
    except:
        return False

def col_with_typ(c):
    return '%s %s' % (c[0], c[1]) if isinstance(c, tuple) else c

def col_without_typ(c):
    return c[0] if isinstance(c, tuple) else c

def debug(msg):
    sys.stderr.write('%s\n' % (msg))

def check_schema(cur, schema):
    for table_name, columns in schema.items():
        try:
            sql = "SELECT %s FROM %s WHERE 1=2" % (
                ', '.join(col_without_typ(c) for c in columns), table_name)
            # debug(sql)
            cur.execute(sql)
        except Exception as e:
            debug(e)
            return False
    return True

def create_schema(cur, schema):
    for table_name, columns in schema.items():
        sql = "CREATE TABLE %s (%s)" % (
            table_name, ', '.join(col_with_typ(c) for c in columns))
        # debug(sql)
        cur.execute(sql)

_con = None
_cur = None
def initialize(data_dir):
    global _con
    global _cur

    _con = sqlite3.connect("%s/mtasks.db" % (data_dir or 'data'))
    _cur = _con.cursor()
    schema = {
        'tasks1': [('id', 'INTEGER PRIMARY KEY'), 'summary', 'ttyp', 'detail'],
        'rels1': [('id', 'INTEGER PRIMARY KEY'), 'tid1', 'tid2', 'rtyp'],
        'history1': [('id', 'INTEGER PRIMARY KEY'), 'ts', 'etyp', 'eid', 'changes']
    }
    if not os.path.exists(data_dir):
        os.makedir(data_dir)
    if not check_schema(_cur, schema):
        create_schema(_cur, schema)
    # Check for previous version and copy data

def finalize():
    _con.close()
   
# Tasks

def now_ts():
    dt_now = datetime.now(tz=timezone.utc)
    return dt_now.timestamp()

class Db:
    task_fields = ['id', 'summary', 'ttyp']
    rel_fields = ['id', 'tid1', 'tid2', 'rtyp']

    def create_history(self, etyp, eid, changes, ts=None):
        sql = 'INSERT INTO history1 (ts, etyp, eid, changes) VALUES (?, ?, ?, ?)'
        params = (ts or now_ts(), etyp, eid, changes)
        _cur.execute(sql, params)

    def get_last_insert_id(self):
        _cur.execute('SELECT last_insert_rowid()')
        return _cur.fetchone()[0]

    def create_task(self, summary):
        ttyp = 'TASK'
        sql = 'INSERT INTO tasks1 (summary, ttyp) VALUES (?, ?)'
        params = (summary, ttyp)
        _cur.execute(sql, params)
        _id = self.get_last_insert_id()
        self.create_history('TASK', _id, "summary:=%s,ttyp:=%s" % (s_quote(summary), s_quote(ttyp)))
        return _id

    def create_rel(self, tid1, tid2, rtyp):
        dt_now = datetime.now(tz=timezone.utc)
        ts_now = dt_now.timestamp()
        sql = 'INSERT INTO rels1 (tid1, tid2, rtyp) VALUES (?, ?, ?)'
        params = (tid1, tid2, rtyp)
        _cur.execute(sql, params)
        _id = self.get_last_insert_id()
        self.create_history('REL', _id, "tid1:=%s,tid2=%s,rtyp:=%s" % (tid1, tid2, rtyp))
        return _id

    def _make_result(self, row, fields):
        return { k: row[i] for i, k in enumerate(fields)}

    def find_task(self, summary):
        sql = 'SELECT %s FROM tasks1 WHERE summary LIKE ?' % (', '.join(self.task_fields))
        params = (summary,)
        _cur.execute(sql, params)
        row = _cur.fetchone()
        return self._make_result(row, self.task_fields)

    def find_rel(self, tid1, tid2, rtyp):
        selects = list()
        params = list()
        for k, v in [('tid1', tid1), ('tid2', tid2), ('rtyp', rtyp)]:
            if v is not None:
                selects.append('%s = ?' % (k))
                params.append(v)

        sql = 'SELECT %s FROM rels1 WHERE %s' % (', '.join(self.rel_fields, ' AND '.join(selects)))

        _cur.execute(sql, params)
        row = _cur.fetchone()
        return self._make_result(row, rel_fields)

    def fetch_all_tasks(self):
        sql = 'SELECT %s FROM tasks1' % (', '.join(self.task_fields))
        _cur.execute(sql)
        for row in _cur:
            yield self._make_result(row, self.task_fields)

    def fetch_all_rels(self):
        sql = 'SELECT %s FROM rels1' % (', '.join(self.rel_fields))
        _cur.execute(sql)
        for row in _cur:
            yield self._make_result(row, self.rel_fields)

    def commit(self):
        _con.commit()
