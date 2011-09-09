from django.forms.models import ModelForm
from prototype.models import Project
from django.forms.widgets import Select

class ProjectForm(ModelForm):
	error_css_class = "error"
	required_css_class = "required"
	
	def as_div(self):
		return self._html_output('<div%(html_class_attr)s>%(label)s %(field)s %(errors)s %(help_text)s</div>', u'', '</div>', '<p class="help">%s</p>', False)
	
	class Meta:
		model = Project
		widgets = {
			'use_html_titles': Select(choices=[(True, "HTML title tags"), (False, "File names")])
		}