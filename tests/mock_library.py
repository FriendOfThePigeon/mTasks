import sys
import commands
from entities import Task, Rel

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

    def upsert_task(self, task):
        if task.id is None:
            task.id = next(self.task_ids)
        self.tasks_table[task.id] = task.to_dict()
        return task

    def create_task(self, summary):
        return self.upsert_task(Task.from_dict({'summary': summary}))

    def upsert_rel(self, rel):
        if rel.id is None:
            rel.id = next(self.rel_ids)
        self.rels_table[rel.id] = rel.to_dict()
        return rel

    def create_rel(self, tid1, tid2, rtyp):
        return self.upsert_rel(Rel.from_dict({'tid1': tid1, 'tid2': tid2, 'rtyp': rtyp}))

    def find_task(self, summary):
        for each in self.tasks_table.values():
            if each['summary'] == summary:
                return each
        return None

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
        # Namespace manipulation
        '<': commands.SetVar(),
        '>': commands.GetVar(),
        # Task manipulation
        '+': commands.Create(mock_db),
        '/': commands.Find(mock_db),
        'subtask': commands.SubtaskOf(mock_db),
        'follows': commands.Follows(mock_db),
    }


