# import viewsets in django
from rest_framework.parsers import JSONParser
from rest_framework import generics,mixins
from main.models import assembly,get_item_estimate_val,plan
from .serializer import *
import json
# impot JSONResponse
from django.http import JsonResponse

class assemblyList(generics.ListAPIView,mixins.CreateModelMixin):
	"""This view provides list, detail, create, retrieve, update
	and destroy actions for Things."""
	lookup_field = 'pk'
	serializer_class = assemblySerializer
	parser_classes = [JSONParser]

	def get_queryset(self):
		return assembly.objects.all()
	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)

class assemblyRUD(generics.RetrieveUpdateDestroyAPIView):
	lookup_field = 'pk'
	serializer_class = assemblySerializer

	def get_queryset(self,**kwargs):
		assembly_id = self.kwargs['pk']
		return assembly.objects.all().filter(pk = assembly_id)

class ItemDescriptionList(generics.ListAPIView):
	"""This view provides list, detail, create, retrieve, update
	and destroy actions for Things."""
	lookup_field = 'pk'
	serializer_class = ItemDescriptionSerializer

	def get_queryset(self):
		return item_description.objects.all().exclude(estimated_value=0)

class planList(generics.ListAPIView,mixins.CreateModelMixin):
	lookup_field = 'pk'
	serializer_class = planSerializer

	def get_queryset(self):
		return plan.objects.all()

	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)

class planRUD(generics.RetrieveUpdateDestroyAPIView):
	lookup_field = 'pk'
	serializer_class = planSerializer

	def get_queryset(self,**kwargs):
		plan_id = self.kwargs['pk']
		return plan.objects.all().filter(pk = plan_id)

def calculate_plan_estimate(request):
	# print(request.GET)
	json_dict = json.loads(json.dumps(request.GET))
	json_dict = json_dict['assembly_json']
	data = json.loads(json_dict)
	total = 0
	for assembly_pk in data:
		# item_obj = item_description.objects.get(pk=item_pk)
		assembly_obj = data[assembly_pk]
		quantity = int(assembly_obj['quantity'])
		total += assembly.objects.get(pk=assembly_pk).estimate_value * quantity

	total = round(total,2)
	return JsonResponse(total,safe=False)

def calculate_assembly_estimate(request):
	# print(request.GET)
	
	json_dict = json.loads(json.dumps(request.GET))
	json_dict = json_dict['item_json']
	data = json.loads(json_dict)
	total = 0
	for item_pk in data:
		# item_obj = item_description.objects.get(pk=item_pk)
		total += get_item_estimate_val(data[item_pk],item_pk)

	# for i in json_dict:
	# 	print(i)
	total = round(total,2)
	return JsonResponse(total,safe=False)
