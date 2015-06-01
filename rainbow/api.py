from fabric.state import env
#from fabric.api import (local, run, sudo, abort, task, cd, puts, require)
from fabtools.require.files import (directory, put)

#alias fabric's env for simple unit-testing of the rainbow api
fabric_env = env

def deploy(artifact_name, remote_path):
    print "deploying artifact: {artifact_name} to {remote_path}"\
        .format(artifact_name=artifact_name, remote_path=remote_path)

    directory(path=remote_path)
    put(local_path=artifact_name, remote_path=remote_path)

def _roll_to_release(release):
    print "cutting-over to release: {release}".format(release=release)

def roll_to_next_release():
    _roll_to_release("next")

def roll_to_prev_release():
    _roll_to_release("prev")
