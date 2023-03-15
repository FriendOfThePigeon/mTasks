
import commands
from task import Task
from rel import Rel

def gen_ints(start):
    i = start
    while True:
        yield i
        i = i + 1


class MockDb:
    def __init__(self):
        self.tasks_table = {}
        self.task_ids = gen_ints(1)

        self.rels_table = {}
        self.rel_ids = gen_ints(1)

    def create_task(self, summary):
        _id = next(self.task_ids)
        result = {
                'id': _id,
                'summary': summary
                }
        self.tasks_table[_id] = result
        return _id

    def create_rel(self, tid1, tid2, rtyp):
        _id = next(self.rel_ids)
        result = {
                'id': _id,
                'tid1': tid1,
                'tid2': tid2,
                'rtyp': rtyp
                }
        self.rels_table[_id] = result
        return _id

    def find_rel(self, tid1, tid2, rtyp):
        for each in self.rels_table.values():
            if tid1 is not None and tid1 != each['tid1']:
                continue
            if tid2 is not None and tid2 != each['tid2']:
                continue
            if rtyp is not None and rtyp != each['rtyp']:
                continue
            return each
        return None

def mock_library(mock_db):
    return {
        # Stack manipulation
        '\\': commands.Swap(),
        'd': commands.Drop(),
        '.': commands.Dup(),
        '[': commands.Mark(),
        ']': commands.Array(),
        'p': commands.PrintLast(),
        'f': commands.PrintStack(),
        # Task manipulation
        '+': commands.Create(mock_db),
        '/': commands.Find(mock_db),
        'subtask': commands.SubtaskOf(mock_db),
        'follows': commands.Follows(mock_db),
    }


