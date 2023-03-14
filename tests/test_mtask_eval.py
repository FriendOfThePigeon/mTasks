from mtask_eval import mtask_eval
from mock_syntax import mock_syntax

def test_with_parents():
    (stack, _) = mtask_eval(['1', '2', '\\'], mock_syntax)

    assert stack.dump() == ['2', '1']

