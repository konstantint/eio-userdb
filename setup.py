from setuptools import setup, find_packages
import sys, os

import eio_userdb
version = eio_userdb.__version__

setup(name='eio-userdb',
      version=version,
      description="EIO user registration webapp",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='eio flask web registration',
      author='Konstantin Tretyakov',
      author_email='kt@ut.ee',
      url='http://eio.ut.ee/',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points={"console_scripts": ["eioUserDB=eio_userdb:main"]},
      )
