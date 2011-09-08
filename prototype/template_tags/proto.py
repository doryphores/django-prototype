from django.contrib.webdesign.lorem_ipsum import words, paragraphs
from django import template
from django.template import TemplateSyntaxError
from django.template.defaulttags import ForNode

register = template.Library()

#===============================================================================
# JavaScript library tags
# Returns script tag for including jQuery or MooTools libraries from Google CDN
# See http://code.google.com/apis/libraries/devguide.html for available versions
# 
# Supported libraries: jquery, jqueryui and mootools
#===============================================================================

JS_LIBRARIES = {
	'jquery': {False:'jquery.js', True:'jquery.min.js'},
	'jqueryui': {False:'jquery-ui.js', True:'jquery-ui.min.js'},
	'mootools': {False:'mootools.js', True:'mootools-yui-compressed.js'},
}

@register.simple_tag
def jquery(version, minified=False):
	return '<script src="//ajax.googleapis.com/ajax/libs/jquery/%s/%s"></script>' % (
		version,
		JS_LIBRARIES['jquery'][minified],
	)

@register.simple_tag
def mootools(version, minified=False):
	return '<script src="//ajax.googleapis.com/ajax/libs/mootools/%s/%s"></script>' % (
		version,
		JS_LIBRARIES['mootools'][minified],
	)

@register.simple_tag
def jqueryui(version, minified=False):
	return '<script src="//ajax.googleapis.com/ajax/libs/jqueryui/%s/%s"></script>' % (
		version,
		JS_LIBRARIES['jqueryui'][minified],
	)


#===============================================================================
# Repeater tag
#===============================================================================

class RepeatNode(ForNode):
	seq_varname = 'repeat_sequence'
	
	def __init__(self, repeat_count, sequence, nodelist_loop):
		self.repeat_count = int(repeat_count)
		super(RepeatNode, self).__init__('i', sequence, False, nodelist_loop)
	
	def render(self, context):
		context[self.seq_varname] = range(self.repeat_count)
		return super(RepeatNode, self).render(context)

@register.tag(name="repeat")
def repeat(parser, token):
	bits = list(token.split_contents())
	tagname = bits[0]
	if len(bits) < 2:
		raise TemplateSyntaxError("Incorrect format for %r tag: %r" % (tagname, token.contents))
	nodelist_loop = parser.parse(('endrepeat',))
	parser.delete_first_token()
	sequence = parser.compile_filter('repeat_sequence')
	return RepeatNode(bits[1], sequence, nodelist_loop)


#===============================================================================
# Dummy Image tag
# Returns an image placeholder URL from dummyimage.com
#===============================================================================

class DummyImageNode(template.Node):
	def __init__(self, width, height, background, foreground, context_var):
		self.width = width
		self.height = height
		self.background = background
		self.foreground = foreground
		self.context_var = context_var
	
	def render(self, context):
		url = "http://dummyimage.com/%sx%s/%s/%s" %(self.width, self.height, self.background, self.foreground)
		
		if self.context_var:
			context[self.context_var] = url
			return ''
		else:
			return url

@register.tag
def dummyimage(parser, token):
	"""
	Returns an image placeholder URL from dummyimage.com
	
	Usage format::
	
		{% dummyimage width height [background] [foreground] [as image_url] %}
	"""
	bits = list(token.split_contents())
	bit_count = len(bits)
	tagname = bits[0]
	
	background = "000"
	foreground = "FFF"
	varname = None
	
	if bit_count < 3:
		raise TemplateSyntaxError("Incorrect format for '%s' tag" % tagname)
	
	width = bits[1]
	height = bits[2]
	
	if "as" in bits:
		if bits[-1] == "as":
			raise TemplateSyntaxError("Missing variable name for '%s' tag" % tagname)
		varname = bits[-1]
		if bit_count == 7:
			background = bits[3]
			foreground = bits[4]
	else:
		if bit_count == 5:
			background = bits[3]
			foreground = bits[4]
	
	return DummyImageNode(width, height, background, foreground, varname)


#===============================================================================
# Inspector tag
# For inspecting current project mocking data collection
#===============================================================================

class InspectorNode(template.Node):
	def render_value(self, var):
		output = ''
		if isinstance(var, list):
			output += '<ul class="list">'
			for v in var:
				output += '<li>%s</li>' % self.render_value(v)
			output += '</ul>'
		elif isinstance(var, dict):
			output += '<div class="dict"><table>'
			for k, v in var.items():
				output += '<tr><th>%s</th><td>%s</td></tr>' % (k, self.render_value(v))
			output += '</table></div>'
		else:
			output += '%s' % var
		
		return output
	
	def render(self, context):
		data = context["data"]
		
		output = '<ul>'
		
		for k, v in data.items():
			if v:
				output += '<li><h3>%s <span>(%d item%s)</span></h3>%s</li>' % (k, len(v), '' if len(v) == 1 else 's', self.render_value(v))
			else:
				output += '<li><h3 class="error">%s <span>(invalid data structure)</span></h3>' % k
		
		output += '</ul>'
		
		return output

@register.tag
def inspector(parser, token):
	return InspectorNode()



#===============================================================================
# Lorem Ipsum tag
# Modified version of django.contrib.webdesign
# Adds W and T options
#===============================================================================

class LoremNode(template.Node):
	def __init__(self, count, method, common):
		self.count, self.method, self.common = count, method, common

	def render(self, context):
		try:
			count = int(self.count.resolve(context))
		except (ValueError, TypeError):
			count = 1
		if self.method == 'w':
			return words(count, common=self.common)
		if self.method == 's':
			return words(count, common=self.common).capitalize()
		if self.method == 't':
			return words(count, common=self.common).title()
		else:
			paras = paragraphs(count, common=self.common)
		if self.method == 'p':
			paras = ['<p>%s</p>' % p for p in paras]
		return u'\n\n'.join(paras)

@register.tag
def lorem(parser, token):
	"""
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
		* ``{% lorem 3 p %}`` will output the common "lorem ipsum" paragraph
		  and two random paragraphs each wrapped in HTML ``<p>`` tags
		* ``{% lorem 2 w random %}`` will output two random latin words
	"""
	bits = list(token.split_contents())
	tagname = bits[0]
	# Random bit
	common = bits[-1] != 'random'
	if not common:
		bits.pop()
	# Method bit
	if bits[-1] in ('w', 's', 't', 'p', 'b'):
		method = bits.pop()
	else:
		method = 'b'
	# Count bit
	if len(bits) > 1:
		count = bits.pop()
	else:
		count = '1'
	count = parser.compile_filter(count)
	if len(bits) != 1:
		raise template.TemplateSyntaxError("Incorrect format for '%s' tag" % tagname)
	return LoremNode(count, method, common)