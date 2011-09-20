from django.contrib import admin
from prototype.models import Project
from prototype.forms import ProjectForm

class ProjectAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("name",)}
	form = ProjectForm
	list_display = ('name', 'view_link')
	
	def view_link(self, obj):
		return u'<a href="%s">View</a>' % obj.get_absolute_url()
	view_link.allow_tags = True
	view_link.short_description = ""
admin.site.register(Project, ProjectAdmin)