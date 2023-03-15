from mtask_eval import mtask_eval
from mock_library import mock_library, MockDb
from task import Task
from hamcrest import assert_that, equal_to, not_none, instance_of, has_length, contains_inanyorder, all_of, has_entries

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

    result = stack.dump()

    assert_that(result, has_length(1))
    assert_that(mock_db.tasks_table, has_length(2))
    assert_that([each['summary'] for each in mock_db.tasks_table.values()], contains_inanyorder('Parent', 'Child'))
    assert_that(mock_db.rels_table, has_length(1))
    rel = next(a for a in mock_db.rels_table.values())
    assert_that(rel, has_entries({
        'tid1': instance_of(int),
        'tid2': instance_of(int),
        'rtyp': equal_to('SUBTASK')
        }) )
