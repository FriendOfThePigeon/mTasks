
class Entity:
    @classmethod
    def fields(cls):
        raise NotImplementedError()

    @classmethod
    def from_dict(cls, d):
        result = cls()
        for f in cls.fields():
            setattr(result, f, d.get(f))
        result.initialize(d)
        return result

    def to_dict(self):
        return {f: getattr(self, f, None) for f in type(self).fields()}

    def values_tuple(self):
        return tuple(getattr(self, f, None) for f in type(self).fields())

    def initialize(self):
        raise NotImplementedError()


class Task(Entity):
    @classmethod
    def fields(cls):
        return ['id', 'ttyp', 'summary', 'is_complete', 'is_next_action', 'priority', 'due_date']

    @classmethod
    def create(cls, id, summary):
        return cls.from_dict({'id': id, 'summary': summary})

    def initialize(self, d):
        if 'ttyp' not in d:
            self.ttyp = 'TASK'
        if 'is_next_action' not in d:
            self.is_next_action = not self.is_complete

    def __str__(self):
        return 'Task(%s, "%s")' % (self.id, self.summary)

    def __repr__(self):
        return 'Task(%s, "%s")' % (self.id, self.summary)


class Rel(Entity):
    @classmethod
    def fields(cls):
        return ['id', 'tid1', 'tid2', 'rtyp']

    @classmethod
    def create(cls, tid1, tid2, rtyp):
        return cls.from_dict({'tid1': tid1, 'tid2': tid2, 'rtyp': rtyp})

    def initialize(self, d):
        assert self.tid1 is not None and self.tid2 is not None and self.rtyp is not None

    def __str__(self):
        return 'Task(%s, "%s")' % (self.id, self.summary)

    def __repr__(self):
        return 'Task(%s, "%s")' % (self.id, self.summary)


