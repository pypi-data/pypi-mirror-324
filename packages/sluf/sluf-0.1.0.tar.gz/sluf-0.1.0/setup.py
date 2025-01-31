"""
## Development

### release new version

    git commit -am "version bump";git push origin master
    python setup.py --version
    git tag -a v$(python setup.py --version) -m "upgrade";git push --tags

"""

import sys
if (sys.version_info[0]) != (3):
    raise RuntimeError('Python 3 required ')

from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='sluf',
    packages=['sluf']+ [f'sluf.{pkg}' for pkg in find_packages(where='modules')],
    # packages=setuptools.find_packages(
    #     '.',
    #     include=['modules'],
    #     exclude=[
    #         'test','tests', 'unit','deps','data',
    #         'examples','modules_nbs','notebooks*','dist',
    #     ],
    # ),
    package_dir={
        'sluf':'modules',
        # 'sluf.workflow': 'modules/workflow',  # Explicitly
    },
    # entry_points={
    #    "console_scripts": [
    #        "sluf = sluf.run:parser.dispatch",
    #    ],
    #},
)
