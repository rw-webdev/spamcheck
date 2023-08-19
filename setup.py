import os
from setuptools import setup
from spamcheck import VERSION

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# Dynamically calculate the version based on VERSION tuple
if len(VERSION) > 2 and VERSION[2] is not None:
    str_version = "%d.%d.%s" % VERSION[:3]
else:
    str_version = "%d.%d" % VERSION[:2]
version = str_version

setup(
    name='spamcheck',
    version=version,
    description="SpamCheck",
    long_description=README,
    author='RW Dev',
    license='',
    platforms=['any'],
    # packages=find_packages(),
    packages=['spamcheck'],
    include_package_data=True,
    install_requires=['boto3>=1.14.60'],
)
