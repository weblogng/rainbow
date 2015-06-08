import unittest

from mock import patch, call


@patch('fabtools.require.files.directory')
@patch('fabtools.require.files.put')
@patch('fabtools.utils.run_as_root')
@patch('fabric.api.run')
@patch('fabric.api.cd')
class DeployTestCase(unittest.TestCase):

    def test_deploy_puts_the_specified_artifact_to_the_remote_server_and_extracts_it(self, cd, run, run_as_root, put,
                                                                                     directory):
        from rainbow import api

        api.fabric_env.host_string = 'unit-test'
        api.fabric_env.user = 'unit'
        remote_path = "/opt/software"
        artifact_name = "static-webapp-2015-04-18_20-24-25_UTC.35ccbf3.tar.gz"

        directory.return_value = None
        put.return_value = []

        api.deploy(artifact_name, remote_path)

        dest_dir = remote_path + "/static-webapp-2015-04-18_20-24-25_UTC.35ccbf3"

        directory.assert_has_calls([
            call(path=remote_path, use_sudo=True),
            call(path=dest_dir, use_sudo=True, owner='unit')
        ])
        put.assert_called_with(local_path=artifact_name, remote_path=remote_path, use_sudo=True)
        cd.assert_called_with(path=remote_path)

        run.assert_has_calls([
            call("tar -xvf {artifact_name} -C {dest_dir}".format(**locals())),
        ])
        run_as_root.assert_has_calls([
            call("ln -nsf {dest_dir} next".format(**locals()))
        ])

    def test_roll_forward_updates_sym_links(self, cd, run, run_as_root, put, directory):
        from rainbow import api

        api.fabric_env.host_string = 'unit-test'
        api.fabric_env.user = 'unit'

        remote_path = "/opt/software"

        prev_rel_dir = remote_path + "/static-webapp.v1"
        next_rel_dir = remote_path + "/static-webapp.v2"

        run_returns = [prev_rel_dir, next_rel_dir, next_rel_dir]
        def side_effect(*args):
            return run_returns.pop(0)

        run.side_effect = side_effect

        api.roll_to_next_release(remote_path)

        cd.assert_called_with(path=remote_path)
        run.assert_has_calls([
            call("readlink -f {remote_path}/current".format(**locals())),
            call("readlink -f {remote_path}/next".format(**locals())),
        ])
        run_as_root.assert_has_calls([
            call("ln -nsf {prev_rel_dir} prev".format(**locals())),
            call("ln -nsf {next_rel_dir} current".format(**locals()))
        ])

