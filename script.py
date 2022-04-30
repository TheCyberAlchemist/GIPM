from main.models import *

from django.forms import model_to_dict
from copy import deepcopy

def copy_indent_to_new_WO(old_WO, new_WO):
	# copy indent
	
	old_wo = work_order.objects.get(id=old_WO)
	new_wo = work_order.objects.get(id=new_WO)

	indent_list = old_wo.indent_set.all()

	for i in indent_list:

		new_instance = i.clone()
		
		new_instance.id = None
		new_instance.WO = new_wo
		new_instance.PO = None
		new_instance.recived_quantity = 0
		new_instance.recieved = False
		new_instance.locked = False

		new_instance.save()

	print("Copied Successfully ✅✅")
	# print(new_wo.indent_set.all())

# copy_indent_to_new_WO(1, 954)

# if work_order.objects.all().first().indent_set.all().count() == 0:
# 	print("Case 1")
# 	copy_indent_to_new_WO(904,1)
# elif work_order.objects.all().last().indent_set.all().count() == 0:
# 	print("Case 2")
# 	copy_indent_to_new_WO(1, 904)
# else:
# 	print("successfull")