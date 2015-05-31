from nose.tools import *

from rainbow.api import *

def setup():
    print "setting-up"

def teardown():
    print "tearing-down"

def test_deploy():
    deploy()
