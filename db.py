import sqlite3
import os.path
from datetime import datetime, timezone
import sys
from util import s_quote
from entities import Task, Rel
import json

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

def entity_schema(entity):
    f = entity.fields()
    assert f[0] == 'id'
    return [('id', 'INTEGER PRIMARY KEY')] + f[1:]

_con = None
_cur = None
def initialize(data_dir):
    global _con
    global _cur

    _con = sqlite3.connect("%s/mtasks.db" % (data_dir or 'data'))
    _cur = _con.cursor()
    schema = {
        'transactions': [('id', 'INTEGER PRIMARY KEY'), 'ts'],
        'history': [('id', 'INTEGER PRIMARY KEY'), 'ts', 'txid', 'etyp', 'eid', 'changes']
    }
    for table_name, entity in [('tasks', Task), ('rels', Rel)]:
        schema[table_name] = entity_schema(entity)

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

class Tx:
    def __init__(self, _id, ts):
        self.id = _id
        self.ts = ts

def fetch_sql(table_name):
    result = 'SELECT * FROM %s WHERE id = ?' % (table_name)
    sys.stderr.write('SQL: %s\n' % (result))
    return result

def insert_sql(table_name, fields):
    result = 'INSERT INTO %s (%s) VALUES (%s)' % (
            table_name,
            ', '.join(f for f in fields),
            ', '.join('?' for f in fields)
            )
    sys.stderr.write('SQL: %s\n' % (result))
    return result

class Db:
    def get_last_insert_id(self):
        _cur.execute('SELECT last_insert_rowid()')
        return _cur.fetchone()[0]

    def create_transaction(self):
        ts = now_ts()
        sql = 'INSERT INTO transactions (ts) VALUES (?)'
        params = (ts,)
        _cur.execute(sql, params)
        return Tx(self.get_last_insert_id(), ts)

    def create_history(self, tx, etyp, eid, changes, ts=None):
        sql = 'INSERT INTO history (ts, txid, etyp, eid, changes) VALUES (?, ?, ?, ?, ?)'
        params = (tx.ts, tx.id, etyp, eid, changes)
        _cur.execute(sql, params)

    fetch_task_sql = fetch_sql('tasks')
    insert_task_sql = insert_sql('tasks', Task.fields())

    fetch_rel_sql = fetch_sql('rels')
    insert_rel_sql = insert_sql('rels', Rel.fields())

    def upsert_entity(self, ent, etyp, table_name, fetch_ent_sql, insert_ent_sql):
        existing = None
        if ent.id is not None:
            _cur.execute(fetch_ent_sql, ent.id)
            existing = _cur.fetchone()

        _cur.execute(insert_ent_sql, ent.values_tuple())

        if ent.id is None:
            ent.id = self.get_last_insert_id()

        if existing is None:
            changes = {f: (None, getattr(ent, f)) for f in type(ent).fields()}
        else:
            changes = {f: (existing.get(f), getattr(ent, f)) for f in type(ent).fields()}
            # Only save the changes
            changes = {k: v for k, v in changes.items() if v[0] != v[1]}

        tx = self.create_transaction()
        self.create_history(tx, etyp, ent.id, json.dumps(changes))

        return ent

    def upsert_task(self, task):
        return self.upsert_entity(task, 'TASK', 'tasks', self.fetch_task_sql, self.insert_task_sql)

    def create_task(self, summary):
        return self.upsert_task(Task.from_dict({'summary': summary}))

    def upsert_rel(self, rel):
        return self.upsert_entity(rel, 'REL', 'rels', self.fetch_rel_sql, self.insert_rel_sql)

    def create_rel(self, tid1, tid2, rtyp):
        return self.upsert_rel(Rel.from_dict({'tid1': tid1, 'tid2': tid2, 'rtyp': rtyp}))
                            

    # def update_task(self, task, 
    #     self.is_complete = is_complete
    #     self.is_next_action = not is_complete
    #     self.priority = priority
    #     self.due_date = due_date

    def _make_result(self, row, fields):
        return { k: row[i] for i, k in enumerate(fields)}

    def find_task(self, summary):
        sql = 'SELECT %s FROM tasks WHERE summary LIKE ?' % (', '.join(Task.fields()))
        params = (summary,)
        _cur.execute(sql, params)
        row = _cur.fetchone()
        return self._make_result(row, Task.fields())

    def find_rel(self, tid1, tid2, rtyp):
        selects = list()
        params = list()
        for k, v in [('tid1', tid1), ('tid2', tid2), ('rtyp', rtyp)]:
            if v is not None:
                selects.append('%s = ?' % (k))
                params.append(v)

        sql = 'SELECT %s FROM rels WHERE %s' % (', '.join(Rel.fields(), ' AND '.join(selects)))

        _cur.execute(sql, params)
        row = _cur.fetchone()
        return self._make_result(row, Rel.fields())

    def fetch_all_tasks(self):
        sql = 'SELECT %s FROM tasks' % (', '.join(Task.fields()))
        _cur.execute(sql)
        for row in _cur:
            yield self._make_result(row, Task.fields())

    def fetch_all_rels(self):
        sql = 'SELECT %s FROM rels' % (', '.join(Rel.fields()))
        _cur.execute(sql)
        for row in _cur:
            yield self._make_result(row, Rel.fields())

    def commit(self):
        _con.commit()
