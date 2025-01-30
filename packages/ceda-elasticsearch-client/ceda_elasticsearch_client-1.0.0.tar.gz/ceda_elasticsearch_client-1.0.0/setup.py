

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the relevant file
# with open(path.join(here, 'README.md'), encoding='utf-8') as f:
#    long_description = f.read()
long_description = open(os.path.join(here, "README.md")).read()

setup(
    name='ceda-elasticsearch-client',
    version='1.0.0',
    description='CEDA elasticsearch client',
    long_description=long_description,

    # Author details
    author='Sam Pepler',
    author_email='sam.pepler@stfc.ac.uk',
    license='BSD',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: BSD License',
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
    ],
    packages=['ceda_es_client'],

    package_data={
        'ceda_es_client': ['root-ca.pem'],
    },
    # jar: Need to install Slacker library
    install_requires=['elasticsearch'],
)
