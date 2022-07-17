#!/usr/bin/env python
import setuptools

from django_classified import get_version  # noqa isort:skip

with open("README.md") as fh:
    long_description = fh.read()

setuptools.setup(
    author='Sergey Lyapustin',
    name="django-classified",
    version=get_version().replace(' ', '-'),
    author_email="s.lyapustin@gmail.com",
    description="Django Classified",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/slyapustin/django-classified",
    keywords='django classified',
    packages=setuptools.find_packages(exclude=('demo',)),
    python_requires=">=3.8",
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "django-bootstrap-form",
        "django-filter",
        "Django>=3.2,<4.1",
        "Pillow>=6.0",
        "sorl-thumbnail>=12.6",
        "unidecode",
        # Babel is used for currency formatting
        'Babel>=1.0,<3.0',
    ]
)
