import sys

from fabric.api import *

# noinspection PyUnresolvedReferences
from fabtools.vagrant import vagrant

sys.path.append('../../')
from rainbow.api import (
    deploy, roll_to_next_release, roll_to_prev_release
)

@task
def hostname():
    run('hostname')

@task(name="deploy-next")
def deploy_next(artifact_name):
    deploy(artifact_name=artifact_name, remote_path="/opt/static-webapp")

@task(name="roll-forward")
def roll_forward():
    roll_to_next_release()

@task(name="roll-back")
def roll_backward():
    roll_to_prev_release()