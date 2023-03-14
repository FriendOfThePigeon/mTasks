from namespace import Namespace

def test_with_parents():
    ns1 = Namespace(None, {'name': 'one'})
    ns2 = Namespace(ns1, {'name': 'two'})
    ns3 = Namespace(ns2, {'name': 'three'})

    result = [ns.get('name') for ns in ns3.with_parents()]

    assert result == ['three', 'two', 'one']

