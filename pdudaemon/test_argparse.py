import pytest
from . import parse_extra_args

def test_extra1():
    conf = parse_extra_args(['--key=val'])
    assert(conf['key'] == 'val')

def test_extra2():
    conf = parse_extra_args(['--key', 'val'])
    assert(conf['key'] == 'val')

def test_extra_fail():
    with pytest.raises(Exception):
        parse_extra_args(['--key', 'val', 'more=fail'])

def test_extra_fail():
    with pytest.raises(Exception):
        parse_extra_args(['--key'])
