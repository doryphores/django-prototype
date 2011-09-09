from django.contrib import admin
from prototype.models import Project
from prototype.forms import ProjectForm

class ProjectAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("name",)}
	form = ProjectForm
admin.site.register(Project, ProjectAdmin)