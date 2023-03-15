
class Rel:
    def __init__(self, tid1, tid2, rtyp):
        self.tid1 = tid1
        self.tid2 = tid2
        self.rtyp = rtyp

    def __str__(self):
        return 'Rel(%s, %s, %s)' % (self.tid1, self.tid2, self.rtyp)

    def __repr__(self):
        return 'Rel(%s, %s, %s)' % (self.tid1, self.tid2, self.rtyp)



