from distutils.core import setup

setup(
    name='rainbow-deploy',
    version='0.1-dev',
    description='simple blue-green deployment fabric api for file archives',
    author='Stephen Kuenzli',
    author_email='skuenzli@weblogng.com',
    requires=['Fabric', 'fabtools', 'nose'],
    packages=['rainbow'])