#!/usr/bin/env python
import os, sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_mesh_test_project.settings'
test_dir = os.path.dirname(__file__)
sys.path.insert(0, test_dir)

from django.core.management import call_command

def runtests():
	call_command('test')
	sys.exit()

if __name__ == '__main__':
	runtests()
