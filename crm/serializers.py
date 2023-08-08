from rest_framework import serializers
from .models import Lead

class LeadSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Lead
		fields = ('id', 'name', 'phone','email','project_name','facebook_id')
