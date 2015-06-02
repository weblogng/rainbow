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

        artifact_name = "static-webapp-2015-04-18_20-24-25_UTC.35ccbf3.tar.gz"
        remote_path = "/opt/software"
        api.fabric_env.host_string = 'unit-test'
        api.fabric_env.user = 'unit'
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

