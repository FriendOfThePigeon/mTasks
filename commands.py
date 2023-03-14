import sys
import db
from task import Task
from rel import Rel

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

# Task manipulation

class Create(Command):
    def eval(self, namespace, stack):
        desc = stack.pop()
        raw_result = db.create_task(desc)
        result = Task(raw_result)
        stack.push(result)

class Find(Command):
    def eval(self, namespace, stack):
        key = stack.pop()
        result = db.find_task(key)
        stack.push(result)

class SubtaskOf(Command):
    def eval(self, namespace, stack):
        child = stack.pop()
        parent = stack.pop()
        assert isinstance(parent, Task)
        assert isinstance(child, Task)
        result = db.create_rel(parent, child, 'SUBTASK')
        stack.push(result)

class Follows(Command):
    def eval(self, namespace, stack):
        second = stack.pop()
        first = stack.pop()
        assert isinstance(first, Task)
        assert isinstance(second, Task)
        result = db.create_rel(first, second, 'FOLLOWS')
        parent = db.find_rel(None, first.id, 'SUBTASK')
        if parent:
            db.create_rel(parent, second, 'SUBTASK')
        stack.push(second)

class Precedes(Command):
    def eval(self, namespace, stack):
        second = stack.pop()
        first = stack.pop()
        assert isinstance(first, Task)
        assert isinstance(second, Task)
        result = db.create_rel(second.id, first.id, 'FOLLOWS')
        parent = db.find_rel(None, first.id, 'SUBTASK')
        if parent:
            db.create_rel(parent, second, 'SUBTASK')
        # FIXME
        # if first.is_next_action:
        #     second.set_next_action(True)
        #     first.set_next_action(False)
        stack.push(second)

# Process control

class Quit(Command):
    def eval(self, namespace, stack):
        sys.exit(0)
