# DCF is a Django Classified App



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
    * generating META description and meta keywords
    * sitemap.xml
    * robots.txt
    * RSS feed
    * Google Analytics integration

## Requirements
 
* Python 2.7+
* Django 1.8
* [Python Social Auth](https://github.com/omab/python-social-auth/)

## Design

* [Twitter Bootstrap Jumbotron] (http://getbootstrap.com/examples/jumbotron-narrow/)

## Credits:

* [Leveraging HTML and Django Forms: Pagination of Filtered Results](http://schinckel.net/2014/08/17/leveraging-html-and-django-forms%3A-pagination-of-filtered-results/) 
* [Currency field implementation in Django](http://stackoverflow.com/questions/2013835/django-how-should-i-store-a-money-value) 
    
## Installation

* pip install -r requirements.txt
* python ./manage.py syncdb
* python ./manage.py collectstatic
* python ./manage.py runserver


## Customization:
 
 You can provide additional customization in DCF dictionary from settings.py
 
## Demo sites
 * [http://craiglists.ru/](http://craiglists.ru?utm_source=github/)

## TODO

* search improvement
* tests