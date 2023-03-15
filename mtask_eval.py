
from commands import Command
from stacky import Stack
from namespace import Namespace 

def mtask_eval(words, library):
    stack = Stack()
    namespace = Namespace(None, library)
    for w in words:
        a = namespace.get(w)
        if isinstance(a, Command):
            a.eval(namespace, stack)
        else:
            stack.push(w)
    return (stack, namespace)
