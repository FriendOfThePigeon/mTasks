import sys
import db
from entities import Task, Rel

class Command:
    def eval(self, namespace, stack):
        raise NotImplementedError()

    def __str__(self):
        return type(self).__name__

    def __repr__(self):
        return type(self).__name__

# Stack manipulation

class Swap(Command):
    def eval(self, namespace, stack):
        stack.swap()
       
class Drop(Command):
    def eval(self, namespace, stack):
        stack.drop()

class Dup(Command):
    def eval(self, namespace, stack):
        stack.dup()

class Mark(Command):
    def eval(self, namespace, stack):
        stack.mark()

class Array(Command):
    def eval(self, namespace, stack):
        return stack.array()

class PrintLast(Command):
    def eval(self, namespace, stack):
        stack.print_last()

class PrintStack(Command):
    def eval(self, namespace, stack):
        stack.print_all()

# Namespace manipulation

class SetVar(Command):
    def eval(self, namespace, stack):
        name = stack.pop()
        subject = stack.pop()
        namespace.set_local(name, subject)
        stack.push(subject)

class GetVar(Command):
    def eval(self, namespace, stack):
        name = stack.pop()
        subject = namespace.get(name)
        stack.push(subject)

# Task manipulation

class DbCommand(Command):
    def __init__(self, db):
        super().__init__()
        self.db = db

class Create(DbCommand):
    def eval(self, namespace, stack):
        summary = stack.pop()
        result = self.db.create_task(summary)
        # result = Task.create(tid, summary)
        stack.push(result)

class Find(DbCommand):
    def eval(self, namespace, stack):
        key = stack.pop()
        found = self.db.find_task(key)
        result = Task.create(found['id'], found['summary']) if found else None
        stack.push(result)

class SubtaskOf(DbCommand):
    def eval(self, namespace, stack):
        child = stack.pop()
        parent = stack.pop()
        assert isinstance(parent, Task)
        assert isinstance(child, Task)
        self.db.create_rel(parent.id, child.id, 'SUBTASK')

class Follows(DbCommand):
    def eval(self, namespace, stack):
        second = stack.pop()
        first = stack.pop()
        assert isinstance(first, Task)
        assert isinstance(second, Task)
        self.db.create_rel(first.id, second.id, 'FOLLOWS')
        parent = self.db.find_rel(None, first.id, 'SUBTASK')
        if parent:
            self.db.create_rel(parent.tid1, second.id, 'SUBTASK')

class Precedes(DbCommand):
    def eval(self, namespace, stack):
        second = stack.pop()
        first = stack.pop()
        assert isinstance(first, Task)
        assert isinstance(second, Task)
        self.db.create_rel(second.id, first.id, 'FOLLOWS')
        parent = self.db.find_rel(None, first.id, 'SUBTASK')
        if parent:
            self.db.create_rel(parent.tid1, second.id, 'SUBTASK')
        # FIXME
        # if first.is_next_action:
        #     second.set_next_action(True)
        #     first.set_next_action(False)

class Commit(DbCommand):
    def eval(self, namespace, stack):
        self.db.commit()


# Process control

class Quit(Command):
    def eval(self, namespace, stack):
        sys.exit(0)
