#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import join, dirname
from setuptools import setup, find_packages

setup(
    name='django-x_file_accel_redirects',
    version='0.0.1',
    packages=find_packages(),
    requires=['python (>= 2.7)', 'django_model_utils'],
    install_requires=['django-model-utils<1.4.0'],
    tests_require=['mock'],
    description='Django app to easy configuration of multiple X-File-Accel locations',
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
    author='42 Coffee Cups',
    author_email='contact@42cc.co',
    url='https://github.com/42cc/django-x-file-accel',
    download_url='https://github.com/42cc/django-x-file-accel/archive/master.zip',
    license='BSD License',
    keywords=['ripple', 'api'],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
    ],
)
