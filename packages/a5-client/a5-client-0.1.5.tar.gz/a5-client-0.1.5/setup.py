from setuptools import setup, find_packages

setup(
    name='a5-client',
    version='0.1.5',
    packages=find_packages(),
    description='a5 API client',
    author='Juan F. Bianchi',
    author_email='jbianchi@ina.gob.ar',
    url='https://github.com/jbianchi81/a5_client',
    install_requires=[
        'a5_client_utils',
        'pandas',
        'jsonschema',
        'requests',
        'datetime',
        'pyyaml'
    ]
)