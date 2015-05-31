from fabric.api import *

# noinspection PyUnresolvedReferences
from fabtools.vagrant import vagrant

@task
def hello():
    run('echo "hello world"')

@task
def uname():
    run('uname -a')
