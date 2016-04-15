# DCF is a Django Classified Advertising App


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
    * Compress CSS/JS (via [Django Compressor](https://github.com/django-compressor/django-compressor))
    * [Open Graph protocol](http://ogp.me/) support
* Caching
* Translation
    * EN - basic version
    * Russian 
    * French (thanx to [Teolemon](https://github.com/teolemon))

## Requirements
 
* Python 2.7+
* Django 1.9
* [Python Social Auth](https://github.com/omab/python-social-auth/)

## Design

* [Twitter Bootstrap Jumbotron](http://getbootstrap.com/examples/jumbotron-narrow/)

## Credits:

* [Leveraging HTML and Django Forms: Pagination of Filtered Results](http://schinckel.net/2014/08/17/leveraging-html-and-django-forms%3A-pagination-of-filtered-results/) 
    
## Installation

    pip install -r requirements.txt
    python ./manage.py migrate
    python ./manage.py createsuperuser
    python ./manage.py runserver
    
Visit [Admin Page](http://localhost:8000/admin/) and create some Sections/Group

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
 
## Demo sites
 * [http://craiglists.ru/](http://craiglists.ru?utm_source=github)
 * Hosted at [Digital Ocean](https://m.do.co/c/08ce1ee690de)

## TODO

* search improvement
* favorites