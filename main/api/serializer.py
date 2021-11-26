from rest_framework import serializers
from main.models import assembly,item_description

class assemblySerializer(serializers.ModelSerializer):
	class Meta:
		model = assembly
		fields = '__all__'
		read_only_fields = ['id']

class ItemDescriptionSerializer(serializers.ModelSerializer):
	class Meta:
		model = item_description
		fields = ['id','description','estimated_value']
		read_only_fields = ['id']