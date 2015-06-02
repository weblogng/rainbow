from fabric.state import env
from fabtools.require.files import (directory, put)
from fabtools.utils import (run_as_root)
from fabric.api import (cd, run)

#alias fabric's env for simple unit-testing of the rainbow api
fabric_env = env

def deploy(artifact_name, remote_path):
    artifact_name = str(artifact_name)
    remote_path = str(remote_path)
    print "deploying artifact: {artifact_name} to {remote_path}"\
        .format(artifact_name=artifact_name, remote_path=remote_path)

    dest_dir = remote_path + "/"

    if artifact_name.endswith(".tar.gz"):
        dest_dir = dest_dir + artifact_name[:(-1 * len(".tar.gz"))]
    else:
        dest_dir = dest_dir + artifact_name

    # note: the request to create the remote_path should be superfluous since dest_dir contains it
    directory(path=remote_path, use_sudo=True)
    directory(path=dest_dir, use_sudo=True, owner=fabric_env.user)

    put(local_path=artifact_name, remote_path=remote_path, use_sudo=True)

    with cd(path=remote_path):
        run("tar -xvf {artifact_name} -C {dest_dir}".format(dest_dir=dest_dir, artifact_name=artifact_name))
        run_as_root("ln -nsf {dest_dir} next".format(dest_dir=dest_dir))

def _roll_to_release(release):
    print "cutting-over to release: {release}".format(release=release)

def roll_to_next_release():
    _roll_to_release("next")

def roll_to_prev_release():
    _roll_to_release("prev")
