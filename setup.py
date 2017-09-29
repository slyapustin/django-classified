#!/usr/bin/env python
import os
from distutils.core import setup


def get_requirements():
    with open(os.path.join(os.path.dirname(__file__), "dcf/requirements.txt")) as f:
        requirements_list = [req.strip() for req in f.readlines()]

    return requirements_list


setup(
    name='dcf',
    version='0.3',
    description='Django Classifieds Application',
    url='https://github.com/inoks/dcf',
    author='Inoks <inoks@mail.ru>',
    author_email='inoks@mail.ru',
    install_requires=get_requirements(),
)
