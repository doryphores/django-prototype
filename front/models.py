from django.db import models

class Project(models.Model):
	name = models.CharField(max_length=255)
	slug = models.SlugField(max_length=255)
	
	def __unicode__(self):
		return u'%s' % self.name
	
	class Meta:
		ordering = ['name']
		