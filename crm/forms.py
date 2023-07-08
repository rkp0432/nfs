from django import forms
from .models import *

class LeadForm(forms.ModelForm):
	class Meta:
		model = Lead
		fields = ('name', 'phone', 'email', 
			'project_name', 'project_location', 'project_type', 'project_completion_status', 
			'budget', 'status', 'initial_observation')