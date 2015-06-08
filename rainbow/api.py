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

    file_extension = '.tar.gz'
    bare_artifact_name = artifact_name
    if artifact_name.endswith(file_extension):
        bare_artifact_name = artifact_name[:(-1 * len(file_extension))]
        dest_dir = dest_dir + bare_artifact_name
    else:
        dest_dir = dest_dir + artifact_name

    if bare_artifact_name in ['prev', 'current', 'next']:
        raise ValueError("sorry, {artifact_name} is not a legal artifact name because it collides "
                         "with a word reserved for symbolic links used by rainbow".format(artifact_name=artifact_name))

    # note: the request to create the remote_path should be superfluous since dest_dir contains it
    directory(path=remote_path, use_sudo=True)
    directory(path=dest_dir, use_sudo=True, owner=fabric_env.user)

    put(local_path=artifact_name, remote_path=remote_path, use_sudo=True)

    with cd(path=remote_path):
        run("tar -xvf {artifact_name} -C {dest_dir}".format(dest_dir=dest_dir, artifact_name=artifact_name))
        run_as_root("ln -nsf {dest_dir} next".format(dest_dir=dest_dir))

def _roll_to_release(release, remote_path):
    print "cutting-over to release: {release}".format(release=release)

    with cd(path=remote_path):
        print "changed to {remote_path}".format(remote_path=remote_path)
        current_rel = run("readlink -f {remote_path}/current".format(remote_path=remote_path))
        target_rel = run("readlink -f {remote_path}/{release}".format(remote_path=remote_path, release=release))

        run_as_root("ln -nsf {current_rel} prev".format(current_rel=current_rel))
        run_as_root("ln -nsf {target_rel} current".format(target_rel=target_rel))

        current_rel = run("readlink -f {remote_path}/current".format(remote_path=remote_path))
        print "updated current release to {current_rel}".format(current_rel=current_rel)


def roll_to_next_release(remote_path):
    _roll_to_release("next", remote_path)

def roll_to_prev_release(remote_path):
    _roll_to_release("prev", remote_path)
