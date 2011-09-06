## Overview

I like to write HTML templates separately from the main app and keep the front-end code in its own repository.
I used to use a combination of server side includes (SSI) and Ant scripts for speeding up the process and exporting
the optimised assets to the main app repository.

This is an attempt to improve on the initial concept while developing my python and django skills.

This app is tightly coupled with a specific Apache configuration using vhost aliases to serve django templates from
anywhere on the developer's machine.

On top of the standard django template tags and filters django-prototype adds the following prototyping tags:

### repeat

Repeats the HTML fragment n times.

Usage format:

{% repeat n %}
	... HTML fragment ...
	{% endrepeat %}

### dummyimage

Inserts an image placeholder from [dummyimage.com](http://dummyimage.com)

Usage format:
	
	{% dummyimage width height [background] [foreground] [as image_url] %}

``width`` and ``height`` are self explanatory

``background`` and ``foreground`` are hex code values for the placeholder colors

if ``image_url`` is provided, the tag writes the url to this variable instead of outputting the ``<img>`` tag

### lorem

An improved version of the lorem tag included in django.contrib.webdesign

Creates random Latin text useful for providing test data in templates.

Usage format::

	{% lorem [count] [method] [random] %}

``count`` is a number (or variable) containing the number of paragraphs or
words to generate (default is 1).

``method`` is either ``w`` for words, ``s`` for a capitalized sentence,
``t`` for a title cased sentence, ``p`` for HTML paragraphs, ``b`` for
plain-text paragraph blocks (default is ``b``).

``random`` is the word ``random``, which if given, does not use the common
paragraph (starting "Lorem ipsum dolor sit amet, consectetuer...").

Examples:
 * ``{% lorem %}`` will output the common "lorem ipsum" paragraph
 * ``{% lorem 3 p %}`` will output the common "lorem ipsum" paragraph and two random paragraphs each wrapped in HTML ``<p>`` tags
 * ``{% lorem 2 w random %}`` will output two random latin words

## Python requirements

Tested on **python 2.6.4**.

The following libraries are required:

 * django 1.3
 * jsmin
 * cssmin
 * south

## Apache configuration

The following Apache modules are required:

 * mod_wsgi
 * mod_rewrite
 * mod_alias
 * mod\_vhost\_alias 

### Windows

Virtual host configuration:

	<VirtualHost *:80>
		# Admin host name
		ServerName prototype.django.local
		# Alias for individual projects
		ServerAlias *.proto.local
		
		UseCanonicalName Off
		
		# Set document root to template project (from subdomain or server alias)
		VirtualDocumentRoot "/path/to/template/projects/%1/www"
		
		# Add support for wsgi scripts
		AddHandler wsgi-script wsgi
		
		# Aliases for django app and static files
		Alias /app "/path/to/django-prototype/public"
		Alias /media "/path/to/django-prototype/public/media"
		Alias /static "/path/to/django-prototype/public/static"
		
		RewriteEngine On
		
		# Direct requests to django app if not static assets
		RewriteCond %{REQUEST_FILENAME} !-f
		RewriteCond %{REQUEST_URI} !^/(static|media|assets|favicon|icons|error)
		RewriteRule ^(.*)$ /app/connector.wsgi/$1 [QSA,PT,L]
	</VirtualHost>