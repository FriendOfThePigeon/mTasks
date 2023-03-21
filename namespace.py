
class Namespace:
    def __init__(self, parent, initial):
        self._parent = parent
        self._dict = dict(initial) if initial else dict()

    def with_parents(self):
        yield self
        if self._parent:
            for each in self._parent.with_parents():
                yield each

    def has(self, key):
        return key in self._dict

    def get(self, key):
        if key in self._dict:
            return self._dict[key]   
        if self._parent is None:
            return None
            # raise KeyError('Not found: %s' % (key))
        return self._parent.get(key)

    def get_local(self, key):
        return self._dict.get(key)

    def set_local(self, key, value):
        self._dict[key] = value

    def set_in_scope(self, key, value):
        for env in self.with_parents():
            last = env
            if env.has(key):
                env.set_local(key, value)
                return
        self.set_local(key, value)




