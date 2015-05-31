import unittest

from mock import patch

@patch('fabtools.require.files.put')
class DeployTestCase(unittest.TestCase):

# in tests package

    def test_deploy_puts_the_specified_artifact_to_the_remote_server(self, put):
        from rainbow import api
        artifact_name = "static-webapp-2015-04-18_20-24-25_UTC.35ccbf3.tar.gz"
        remote_path = "/opt/software"
        api.fabric_env.host_string = 'unit-test'
        put.return_value = []

        api.deploy(artifact_name, remote_path)

        put.assert_called_with(local_path=artifact_name, remote_path=remote_path)
