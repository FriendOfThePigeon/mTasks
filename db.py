import sqlite3
import os.path
from datetime import datetime, timezone

def check_table(cur, table_name, columns):
    try:
        cur.execute("SELECT %s FROM %s WHERE 1=2" % (', '.join(columns), table_name))
        return True
    except:
        return False

def check_schema(cur, schema):
    
    for table_name, columns in schema.items():
        try:
            cur.execute("SELECT %s FROM %s WHERE 1=2" % (', '.join(columns), table_name))
        except:
            return False
    return True

def create_schema(cur, schema):
    for table_name, columns in schema.items():
        cur.execute("CREATE TABLE %s (%s)" % (table_name, ', '.join(columns)))

_con = None
_cur = None
def initialize(data_dir):
    global _con
    global _cur

    _con = sqlite3.connect("%s/mtasks.db" % (data_dir or 'data'))
    _cur = con.cursor()
    schema = {
        'tasks1': [('id', 'INTEGER PRIMARY KEY'), 'summary', 'ttyp', 'detail'],
        'rels1': [('id', 'INTEGER PRIMARY KEY'), 'tid1', 'tid2', 'rtyp'],
        'history1': [('id', 'INTEGER PRIMARY KEY'), 'etyp', 'eid', 'changes']
    }
    if not os.path.exists(data_dir):
        os.makedir(data_dir)
    if not check_schema(_cur, schema):
        create_schema(_cur, schema)
    # Check for previous version and copy data

def finalize():
    _con.close()
   
# Tasks

def create_task(summary):
    dt_now = datetime.now(tz=timezone.utc)
    ts_now = dt_now.timestamp()
    sql = 'INSERT INTO tasks1 (summary, ttyp, created, updated) VALUES (?, ?, ?, ?); SELECT last_insert_rowid()'
    params = (summary, 'TASK', ts_now, ts_now)
    _cur.execute(sql, parameters=params)
    row = _cur.fetchone()

def create_rel(id1, id2, rtyp):
    raise NotImplementedError()

def find_task(summary):
    raise NotImplementedError()

def find_rel(id1, id2, rtyp):
    raise NotImplementedError()

