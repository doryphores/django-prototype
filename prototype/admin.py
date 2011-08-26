from django.contrib import admin
from prototype.models import Project

class ProjectAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("name",)}

admin.site.register(Project, ProjectAdmin)