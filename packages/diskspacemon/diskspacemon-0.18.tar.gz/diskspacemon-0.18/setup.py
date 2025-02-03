from __future__ import print_function
from setuptools import setup
from pathlib import Path
import os, sys
import shutil

NAME = "diskspacemon"

def get_version():
    """Get version and version_info without importing the entire module."""
    # print("NAME:", NAME)
    path = str(Path(__file__).parent / '__meta__.py')

    if sys.version_info.major == 3:
        import importlib.util

        spec = importlib.util.spec_from_file_location("__meta__", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        vi = module.__version_info__
        return vi._get_canonical(), vi._get_dev_status()
    else:
        import imp
        vi = imp.load_source("meat", "__meta__.py")
        return vi.__version__, vi.__status__

def get_requirements(req):
    """Load list of dependencies."""

    install_requires = []
    with open(req) as f:
        for line in f:
            if not line.startswith("#"):
                install_requires.append(line.strip())
    return install_requires


def get_description():
    """Get long description."""

    desc = ''

    if os.path.isfile('README.md'):
        with open("README.md", 'r') as f:
            desc = f.read()
    return desc

VER, DEVSTATUS = get_version()

try:
    os.remove(os.path.join(NAME, '__version__.py'))
except:
    pass
shutil.copy2('__version__.py', NAME)

import __version__
version = __version__.version

if sys.version_info.major == 3:
    entry_points = {
         "console_scripts": ["diskspacemon3 = diskspacemon:__main__.usage", "diskspacemon = diskspacemon:__main__.usage"]
    }
else:
    entry_points = {
         "console_scripts": ["diskspacemon = diskspacemon:__main__.usage",]
    }

setup(
    name=NAME,
    version=version,
    author = 'Hadi Cahyadi LD',
    author_email = 'cumulus13@gmail.com',
    maintainer="cumulus13 Team",
    maintainer_email="cumulus13@gmail.com",    
    description = ('Monitoring space of directory/path/drive then send notification to growl and syslog/remote syslog with multiple host and port'),
    license = 'MIT',
    keywords = "disk space monitor growl syslog",
    url = 'https://github.com/cumulus13/diskspacemon',
    project_urls={
        "Documentation": "https://github.com/cumulus13/diskspacemon",
        "Code": "https://github.com/cumulus13/diskspacemon",
    },
    packages = [NAME],
    download_url = 'https://github.com/cumulus13/diskspacemon/tarball/master',
    install_requires=[
        'sendgrowl',
        'argparse',
        'configset',
        'pydebugger',
        'ctraceback',
        'bitmath',
        'json5'
    ],
    entry_points = entry_points,
    package_data={'': ['__version__.py', 'monitor.ini']},
    include_package_data=True,
    python_requires=">=3.0",    
    classifiers=[
        'Development Status :: %s' % DEVSTATUS,
        'Environment :: Console',
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    long_description=get_description(),
    long_description_content_type="text/markdown",
)
