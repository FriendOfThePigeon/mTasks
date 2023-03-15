from commands import DbCommand
from util import d_quote

class DotCommand(DbCommand):
    def eval(self, namespace, stack):
        print('digraph tasks {')
        print('rankdir="LR"')
        print('node[shape="box"]')
        for t in self.db.fetch_all_tasks():
            print('n%s[label=%s];' % (t['id'], t['summary']))
        for r in self.db.fetch_all_rels():
            print('n%s->n%s[label=%s];' % (r['tid1'], r['tid2'], r['rtyp']))
        print('}')

