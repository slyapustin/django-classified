# Django Classified Advertising Application

[![Build Status](https://travis-ci.org/inoks/django-classified.svg?branch=master)](https://travis-ci.org/inoks/django-classified)

## Features

* User registration
 * via social networks (Facebook as example)
* Item groups and categories
* Image
    * upload multiple images per item
    * generating preview (via [sorl-thumbnail](https://github.com/mariocesar/sorl-thumbnail))
    * display using [Lightbox JS](http://lokeshdhakar.com/projects/lightbox2/) library
* Search ability
* SEO optimisation
    * SEO-friendly urls 
    * generating META description and meta keywords
    * sitemap.xml
    * robots.txt
    * RSS feed
    * Google Analytics integration
    * [Open Graph protocol](http://ogp.me/) support
* Caching
* Translation
    * English
    * Russian 
    * French (thanks to [Teolemon](https://github.com/teolemon))
    * Turkish (thanks to [Mirat Can Bayrak](https://github.com/miratcan))
    * Help translate to other languages at [Transifex](https://www.transifex.com/inoks/dcf/)

## Requirements
 
* Python 2.7, 3.5, 3.6
* Django 1.11, 2.0

## Design

* [Twitter Bootstrap Jumbotron](http://getbootstrap.com/examples/jumbotron-narrow/)

## Demo project

Demo project available at `demo/` folder.

## Installation
 * Install app `pip install django-classified`
 * Add `django-classified` to the `INSTALLED_APPS` list
 * Add `url(r'', include('django_classified.urls', namespace='django_classified')),` to the project `urls.py` file.
 * Add `'django_classified.context_processors.common_values'` to the `context_processors` list


## Customization:
 
 You can provide additional customization in settings.py
 
 * DCF_SITE_NAME - Site title
 * DCF_SITE_DESCRIPTION - Site description
 * DCF_ITEM_PER_USER_LIMIT - Max Items allowed per user
 * DCF_SITEMAP_LIMIT - Sitemap items limit 
 * DCF_RSS_LIMIT - RSS feed items limit
 * DCF_RELATED_LIMIT - Number of related items displayed
 * DCF_ITEM_PER_PAGE - Number of items per page
 * DCF_LOGIN_TO_CONTACT - Hide contact information for unauthorized requests

## Credits

 * Thanks [JetBrains](https://www.jetbrains.com) for the awesome [PyCharm](https://www.jetbrains.com/pycharm/) IDE.
 