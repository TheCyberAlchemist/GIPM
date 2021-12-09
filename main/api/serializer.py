from rest_framework import serializers
from main.models import assembly,item_description,plan

class assemblySerializer(serializers.ModelSerializer):
	class Meta:
		model = assembly
		fields = '__all__'
		read_only_fields = ['id']
# class for plan 
class planSerializer(serializers.ModelSerializer):
	class Meta:
		model = plan
		fields = ["name","description","assemblies","assembly_json","estimate_value"]
		read_only_fields = ['id']

class ItemDescriptionSerializer(serializers.ModelSerializer):
	class Meta:
		model = item_description
		fields = ['id','description','estimated_value']
		read_only_fields = ['id']