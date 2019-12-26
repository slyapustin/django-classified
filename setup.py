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
    description="Django classified ads",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/inoks/django-classified",
    keywords='django classified ads',
    packages=setuptools.find_packages(exclude=('demo',)),
    python_requires=">=3.6",
    include_package_data=True,
    zip_safe=False,
    classifiers=(
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires=[
        "django-bootstrap-form",
        "django-filter",
        "Django>=2.0,<3.1",
        "Pillow>=6.0",
        "sorl-thumbnail>=12.6.0",
        "unidecode",
        # Babel is used for currency formatting
        'Babel>=1.0,<3.0',
    ],
    # Remove dependency links after it will be released https://github.com/jazzband/sorl-thumbnail/pull/604
    dependency_links=[
        'git+https://github.com/jazzband/sorl-thumbnail.git@12.6.0-release#egg=sorl-thumbnail-12.6.0'    
    ]
)
