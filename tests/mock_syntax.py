
import commands

def gen_ints(start):
    i = start
    def result():
        while True:
            yield i
            i = i + 1
    return result
    

tasks_table = {}
task_ids = gen_ints(1)

rels_table = {}
rel_ids = gen_ints(1)

def mock_db_create_task(desc):
    _id = next(task_ids)
    result = {
            'id': _id,
            'desc': desc
            }
    tasks_table[_id] = result
    return result

def mock_db_create_rel(tid1, tid2, rtyp):
    _id = next(rel_ids)
    result = {
            'id': _id,
            'tid1': first,
            'tid2': second,
            'rtyp': rtyp
            }
    rels_table[_id] = result
    return result

def mock_db_find_rel(tid1, tid2, rtyp):
    for each in rels_table.values():
        if tid1 is not None and tid1 != each['tid1']:
            continue
        if tid2 is not None and tid2 != each['tid2']:
            continue
        if rtyp is not None and rtyp != each['rtyp']:
            continue
        return each
    return None

class Create(commands.Command):
    def eval(self, env, stack):
        desc = stack.pop()
        raw_result = mock_db_create_task(desc)
        result = Task(raw_result)
        stack.push(result)

class Find(commands.Command):
    def eval(self, env, stack):
        key = stack.pop()
        result = tasks_table.get(key)
        stack.push(result)

class SubtaskOf(commands.Command):
    def eval(self, env, stack):
        child = stack.pop()
        parent = stack.pop()
        result = mock_db_create_rel(parent, child, 'SUBTASK')
        stack.push(result)

class Follows(commands.Command):
    def eval(self, env, stack):
        second = stack.pop()
        first = stack.pop()
        result = mock_db_create_rel(first, second, 'FOLLOWS')
        parent = mock_db_find_rel(None, first.id, 'SUBTASK')
        if parent:
            mock_db_create_rel(parent, second, 'SUBTASK')
        stack.push(second)

class Precedes(commands.Command):
    def eval(self, env, stack):
        second = stack.pop()
        first = stack.pop()
        result = mock_db_create_rel(second.id, first.id, 'FOLLOWS')
        parent = mock_db_find_rel(None, first.id, 'SUBTASK')
        if parent:
            mock_db_create_rel(parent, second, 'SUBTASK')
        stack.push(second)


mock_syntax = {
    # Stack manipulation
    '\\': commands.Swap(),
    'd': commands.Drop(),
    '.': commands.Dup(),
    '[': commands.Mark(),
    ']': commands.Array(),
    'p': commands.PrintLast(),
    'f': commands.PrintStack(),
    # Task manipulation
    '+': Create(),
    '/': Find(),
    'subtask': SubtaskOf(),
    'follows': Follows(),
}


