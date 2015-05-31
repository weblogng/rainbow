import sys

try:
    # noinspection PyUnresolvedReferences
    from setuptools import setup, find_packages
except ImportError:
    # noinspection PyUnresolvedReferences
    from ez_setup import use_setuptools

    use_setuptools()
    from setuptools import setup, find_packages

from setuptools.command.test import test as TestCommand


class Tox(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import tox

        errno = tox.cmdline(self.test_args)
        sys.exit(errno)

setup(
    name='rainbow-deploy',
    version='0.1-dev',
    description='simple blue-green deployment fabric api for file archives',
    author='Stephen Kuenzli',
    author_email='skuenzli@weblogng.com',
    install_requires=[
        "fabric>=1.7.0",
        'fabtools>=0.19.0',
    ],
    setup_requires=[],
    tests_require=[
        'tox',
        'mock',
        'pytest',
    ],
    cmdclass={
        'test': Tox,
    },
    packages=find_packages(exclude=['ez_setup']),
)