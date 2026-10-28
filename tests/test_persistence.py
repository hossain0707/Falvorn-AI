import sqlite3
import pytest
from falvorn.store import RunStore


def test_durable_run_history_survives_restart(tmp_path):
    path=tmp_path/'runs.db'
    store=RunStore(path)
    store.create('test-1')
    store.state('test-1','running')
    e=store.event('test-1','started',url='https://example.com')
    assert e['seq']==0
    store.event('test-1','observation',title='Example')
    store.state('test-1','completed',{'answer':'ok'})
    recovered=RunStore(path).get('test-1')
    assert recovered['status']=='completed'
    assert recovered['answer']=={'answer':'ok'}
    assert len(recovered['events'])==2
    assert recovered['events'][1]['title']=='Example'


def test_incomplete_runs_marked_interrupted(tmp_path):
    path=tmp_path/'runs.db'
    store=RunStore(path)
    store.create('test-1')
    store.state('test-1','running')
    recovered=RunStore(path).get('test-1')
    assert recovered['status']=='interrupted'
    assert 'restarted' in recovered['error']


def test_monitor_subscriptions_cycle(tmp_path):
    store=RunStore(tmp_path/'runs.db')
    sub=store.add_subscription('sid','https://example.com',900)
    assert sub['enabled']==1
    assert store.subscriptions(due_only=True)[0]['id']=='sid'
    store.mark_subscription('sid',True)
    assert store.subscription('sid')['last_changed']==1
    assert store.subscriptions(due_only=True)==[]
    assert store.update_subscription('sid',False)['enabled']==0
    assert store.update_subscription('sid',True)['enabled']==1
    assert store.delete_subscription('sid') is True
    assert store.subscription('sid') is None
