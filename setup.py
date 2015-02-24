#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import django_mesh

package_name = 'django_mesh'
test_package_name = '%s_test_project' % package_name

def runtests():
    import os
    import sys
    
    import django
    from django.core.management import call_command
    
    os.environ['DJANGO_SETTINGS_MODULE'] = '%s.settings' % test_package_name
    django.setup()
    call_command('test', 'django_admin_smoke_tests')
    call_command('test')
    sys.exit()

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
    url='http://seanhayes.name/',
    download_url='https://github.com/SeanHayes/django-mesh',
    license='GPL',
    packages=[
        package_name,
        test_package_name,
    ],
    include_package_data=True,
    install_requires=['Django>=1.7', 'django-model-utils', 'markdown', 'textile', 'oembed', 'pyembed-markdown', 'pyembed', 'requests','six'],

    tests_require=['django-admin-smoke-tests>=0.1.9', 'mock', 'django-settings-context-processor',],

    test_suite='setup.runtests',
)
