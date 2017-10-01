#!/usr/bin/env python
import os
from distutils.core import setup


def get_requirements():
    with open(os.path.join(os.path.dirname(__file__), "dcf/requirements.txt")) as f:
        requirements_list = [req.strip() for req in f.readlines()]

    return requirements_list


setup(
    author='Inoks <inoks@mail.ru>',
    author_email='inoks@mail.ru',
    description='Django Classifieds Application',
    install_requires=get_requirements(),
    keywords='django classified development bootstrap',
    license='MIT',
    name='dcf',
    url='https://github.com/inoks/dcf',
    version='0.5',
    classifiers=[
        'Development Status :: 3 - Beta',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]
)
