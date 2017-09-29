#!/usr/bin/env python
import os
from distutils.core import setup


def get_requirements():
    with open(os.path.join(os.path.dirname(__file__), "requirements/base.txt")) as f:
        requirements_list = [req.strip() for req in f.readlines()]

    # requirements_list.append("setuptools")
    # requirements_list.append("pytz")
    return requirements_list


setup(
    name='dcf_core',
    version='0.1',
    description='Django Classifieds Application',
    url='https://github.com/inoks/dcf',
    author='Inoks <inoks@mail.ru>',
    author_email='inoks@mail.ru',
    install_requires=get_requirements(),
)
