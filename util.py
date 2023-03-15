
def s_quote(s):
    return "'%s'" % ("''".join(s.split("'")))

def d_quote(s):
    return '"%s"' % ('""'.join(s.split('"')))

