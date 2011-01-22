#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import django_mesh

setup(name='django-mesh',
	version=django_mesh.__version__,
	description="A Django blog.",
	author='Seán Hayes',
	author_email='sean@seanhayes.name',
	classifiers=[
		"Development Status :: 3 - Alpha",
		"Framework :: Django",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: GNU General Public License (GPL)",
		"Operating System :: OS Independent",
		"Programming Language :: Python",
		"Programming Language :: Python :: 2.6",
		"Topic :: Internet :: WWW/HTTP :: Dynamic Content",
		"Topic :: Internet :: WWW/HTTP :: Site Management",
		"Topic :: Software Development :: Libraries",
		"Topic :: Software Development :: Libraries :: Python Modules"
	],
	keywords='django blog',
	url='https://github.com/SeanHayes/django-mesh',
	license='GPL',
	packages=['django_mesh', 'django_mesh.tests',],
	install_requires=['Django>=1.2', 'django-pagination',],
)

