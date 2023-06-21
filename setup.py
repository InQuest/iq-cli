import os
from setuptools import setup

with open("README.md", "r") as fh:
    README = fh.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='iqcli',
    version='1.0.0',
    include_package_data=True,
    py_modules=['iqcli'],
    packages=['iqcli', 'iqcli/api', 'iqcli/lib', 'iqcli/cli'],
    entry_points={'console_scripts': ['iqcli=iqcli.cli:cli']},
    license='GPL',
    description='InQuest platform v3 Python client with CLI interface.',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/InQuest/iq-cli',
    author='InQuest Labs',
    author_email='labs@inquest.net',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Security',
        'Topic :: Software Development :: Libraries',
        'Topic :: Internet',
    ],
)