#!/usr/bin/python
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

import os
from setuptools import setup

# just in case setup.py is launched from elsewhere that the containing directory
originalDir = os.getcwd()
os.chdir(os.path.dirname(os.path.abspath(__file__)))
try:
	setup(
		name = "listenerplugins",
		version = '0.0.1',
		packages = ['plugins'],
		package_dir = {'plugins':'plugins'},
		
		# metadata for upload to PyPI
		author = "Sundry",
		keywords = "plugins",
		url = "http://github.com/benhoff/listenerplugins",
		# more details
		classifiers=['Development Status :: 3 - Alpha',
					 'Intended Audience :: Developers',
					 'Operating System :: OS Independent',
					 'Programming Language :: Python :: 3',
					 'Topic :: Software Development :: Libraries :: Python Modules'],
		platforms='All',
		)
	
finally:
  os.chdir(originalDir)
