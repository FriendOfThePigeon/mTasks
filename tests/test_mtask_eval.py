from mtask_eval import mtask_eval
from mock_library import mock_library, MockDb
from entities import Task
from hamcrest import assert_that, equal_to, not_none, instance_of, has_length, contains_inanyorder, all_of, has_entries, is_not, only_contains, contains_exactly, has_property

def test_basic_eval():
    (stack, _) = mtask_eval(['1', '2', '\\'], mock_library(MockDb()))

    assert stack.dump() == ['2', '1']


def test_create_task():
    mock_db = MockDb()
    (stack, _) = mtask_eval(['Summary', '+'], mock_library(mock_db))

    result = stack.dump()[0]

    assert_that(result, instance_of(Task))
    assert_that(result.id, not_none())
    assert_that(result.summary, equal_to('Summary'))

def test_create_sub_task():
    mock_db = MockDb()
    (stack, _) = mtask_eval(['Parent', '+', 'Child', '+', 'subtask'], mock_library(mock_db))

    assert_that(mock_db.tasks_table, has_length(2))
    assert_that([each['summary'] for each in mock_db.tasks_table.values()], contains_inanyorder('Parent', 'Child'))

    assert_that(mock_db.rels_table, has_length(1))
    rel = next(a for a in mock_db.rels_table.values())
    assert_that(rel, has_entries({
        'tid1': instance_of(int),
        'tid2': instance_of(int),
        'rtyp': equal_to('SUBTASK')
        }) )

def test_vars():
    mock_db = MockDb()
    commands = 'Parent + p1 < Child1 + subtask p1 > Child2 + subtask'.split(' ')
    (stack, ns) = mtask_eval(commands, mock_library(mock_db))

    parent = ns.get_local('p1')
    assert_that(parent, not_none())
    assert_that(parent.summary, equal_to('Parent'))
    tid_parent = parent.id

    assert_that(mock_db.tasks_table, has_length(3))
    assert_that([each['summary'] for each in mock_db.tasks_table.values()], contains_inanyorder('Parent', 'Child1', 'Child2'))

    assert_that(mock_db.rels_table, has_length(2))
    tid2s = set(each['tid2'] for each in mock_db.rels_table.values())
    assert_that(tid2s, has_length(2))
    assert_that(tid2s, only_contains(all_of(not_none(), is_not(equal_to(tid_parent)))))
    assert_that(mock_db.rels_table.values(), only_contains(has_entries({'tid1': tid_parent, 'rtyp': 'SUBTASK'})))

def test_find():
    mock_db = MockDb()
    mtask_eval('TaskOne +'.split(' '), mock_library(mock_db))
    (stack, ns) = mtask_eval('TaskOne /'.split(' '), mock_library(mock_db))

    result = stack.dump()
    assert_that(result, contains_exactly(all_of(not_none(), has_property('summary', 'TaskOne'))))
