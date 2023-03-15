
class Task:
    def __init__(self, _id, summary):
        self.id = _id
        self.summary = summary

    def __str__(self):
        return 'Task(%s, "%s")' % (self.id, self.summary)

    def __repr__(self):
        return 'Task(%s, "%s")' % (self.id, self.summary)


