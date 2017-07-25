from setuptools import setup, find_packages
from data_factory import __version__


def readme():
    with open('README.md') as f:
        return f.read()

reqs = [line.strip() for line in open('requirements.txt')]

GIT_REPO = "https://github.com/ukcp-data/ukcp18-data-factory"

setup(
    name                 = "ukcp18-data-factory",
    version              = __version__,
    description          = "Tools to generate NetCDF4 data files.",
    long_description     = readme(),
    license              = "",
    author               = "Ag Stephens",
    author_email         = "ag.stephens@stfc.ac.uk",
    url                  = GIT_REPO,
    packages             = find_packages(),
    install_requires     = reqs,
    tests_require        = ['pytest'],
    classifiers          = [
        'Development Status :: 2 - ???',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: ???',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
    ],
    include_package_data = True,
    scripts=[],
    entry_points = {},
    package_data = {
        'data_factory': ['test/example_data/*'],
    }
)
