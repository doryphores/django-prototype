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
		VirtualDocumentRoot "c:\path\to\template\projects\%1\www"
		
		# Add support for wsgi scripts
		AddHandler wsgi-script wsgi
		
		# Aliases for django app and static files
		Alias /public "c:\path\to\django-prototype\app\public"
		Alias /media "c:\path\to\django-prototype\public\media"
		Alias /static "c:\path\to\django-prototype\public\static"
		
		RewriteEngine On
		
		# Direct requests to django app if not static assets
		RewriteCond %{REQUEST_FILENAME} !-f
		RewriteCond %{REQUEST_URI} !^/(static|media|assets|favicon|icons|error)
		RewriteRule ^(.*)$ /public/connector.wsgi/$1 [QSA,PT,L]
	</VirtualHost>