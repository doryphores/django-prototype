# django-prototype

## Overview

I like to write HTML templates separately from the main app and keep the front-end code in its own repository.
I used to use a combination of server side includes (SSI) and Ant scripts for speeding up the process and exporting
the optimised assets to the main app repository.

This is an attempt to improve on the initial concept while developing my python and django skills.

This app is tightly coupled with a specific Apache configuration using vhost aliases to serve django templates from
anywhere on the developer's machine.

This is a work in progress. Eventually, I want to add functionality to export optimised CSS and JS assets
so they can be imported into a django app.

## Configuration

### PROTOTYPE_PROJECTS_ROOT

Where template projects are located on the developer's machine. Each project is stored in a folder
named after it's slug in the DB.

### PROTOTYPE_DEFAULT_DATA_PATH

The path relative path to a template project's root in which JSON data files are located. See
Dummy Data information below.

### PROTOTYPE_PROJECTS_HOST

The domain used for accessing template projects. For example, if set to ``proto.local``,
individual projects can be accessed via ``[project_slug].proto.local``. This must reflect
the ``ServerAlias`` setting in the Apache vhost:

	ServerAlias *.proto.local

## Template tags

On top of the standard django template tags and filters django-prototype adds the following prototyping tags:

### repeat

Repeats the HTML fragment ``n`` times.

Usage format:

	{% repeat n %}
	... HTML fragment ...
	{% endrepeat %}

### dummyimage

Inserts an image placeholder URL from [dummyimage.com](http://dummyimage.com)

Usage format:

	{% dummyimage width height [background] [foreground] [as image_url] %}

``width`` and ``height`` are self explanatory

``background`` and ``foreground`` are hex code values for the placeholder colors

if ``image_url`` is provided, the tag writes the URL to this variable instead of outputting it

### wait

Use this tag to simulate server processing time.

Usage format::

	{% wait seconds %}

``seconds`` is the number of seconds to wait before serving the template

### lorem

An improved version of the lorem tag included in django.contrib.webdesign

Creates random Latin text useful for providing test data in templates.

Usage format:

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

### JavaScript library tags

Returns script tag for including jQuery or MooTools libraries from Google CDN

See http://code.google.com/apis/libraries/devguide.html for available versions

Usage format:

	{% jquery version [minified] %}

	{% jqueryui version [minified] %}

	{% mootools version [minified] %}

if ``minified`` is ``1``, loads the minified or compressed version of the library

### inspector

Special tag for displaying the current project's available dummy data structures.

## Dummy data

django-prototype automatically parses the data folder of your project for json files and makes these data
structures available to your templates. By default, the data folder is in the root of your project but this
is configurable on a per-project basis. For example, if you place a json file named ``products`` in the data
folder, the resulting data structure can be used in a for loop in your templates:

	{% for product in project.data.products %}
	...
	{% endfor %}

## Python requirements

Tested on **python 2.6.4**.

The following libraries are required:

 * django 1.4.2

## Apache configuration

The following Apache modules are required:

 * mod_wsgi
 * mod_rewrite
 * mod_alias
 * mod\_vhost\_alias

### Virtual host configuration

	<VirtualHost *:80>
		# Admin host name
		ServerName proto.local
		# Alias for individual projects
		# In the example below, individual projects are accessed via [project_slug].proto.local
		ServerAlias *.proto.local

		UseCanonicalName Off

		# Set document root to template project (from subdomain or server alias)
		# %1 is replaced with first part of server name
		VirtualDocumentRoot /path/to/template/projects/%1

		DocumentRoot /path/to/template/projects

		WSGIScriptAlias /__proto__ /path/to/django-prototype/public/wsgi.py

		RewriteEngine On

		# Direct requests to django app if not static assets
		# icons and error and in there to allow default apache server assets
		RewriteCond %{HTTP_HOST} ^([^\.]+)\.proto\.local$ [NC]
		RewriteCond %{REQUEST_URI} !^/(__proto__)
		RewriteCond %{DOCUMENT_ROOT}/%1%{REQUEST_URI} !-f
		RewriteRule ^(.*)$ /__proto__$1 [QSA,PT,L]
	</VirtualHost>
