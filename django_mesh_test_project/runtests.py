#!/usr/bin/env python
import os, sys
import settings
from django.core.management import call_command

os.environ['DJANGO_SETTINGS_MODULE'] = '%s.settings' % settings.PACKAGE_MODULE
sys.path.insert(0, settings.PACKAGE_PARENT_DIR)

def runtests():
	call_command('test')
	sys.exit()

if __name__ == '__main__':
	runtests()
