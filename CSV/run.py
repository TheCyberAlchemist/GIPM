import sys
# sys.path.append("C:\\Users\\admin\\Desktop\\Somewhere\\dad")
import csv
from main.models import *

with open("C:\\Users\\admin\\Desktop\\Somewhere\\dad\\CSV\\changed_indent.csv") as f:
	reader = csv.reader(f)
	c = 0
	for row in reader:
		if c > 1 and row[0]:
			wo = work_order.objects.filter(wo_number=row[1]).first()
			mt_type = None if row[4] == "NA" else row[4]
			if not row[22].isnumeric():
				description,_ = item_description.objects.get_or_create(description=row[2])
				# description = item_description.objects.filter(description=row[22]).first()
			else:
				description=None
			# applied get_or_create and now just send the new description in the old csv
			int_or_0 = lambda x: float(x) if x else 0
			size = int_or_0(row[7])
			thickness = int_or_0(row[8])
			width = int_or_0(row[9])
			internal_diameter = int_or_0(row[10])
			quantity = int_or_0(row[5])
			value = int_or_0(row[12])
			discount = int_or_0(row[13])
			other_expanses = int_or_0(row[14])
			tax = int_or_0(row[15])
			# print(wo,size,thickness,width,internal_diameter,quantity,value,discount,other_expanses,tax,description)
			created =  indent.objects.create(
				WO=wo,
				recived = False,
				comment=row[2],
				material_shape=row[3],
				material_type=mt_type,
				item_description=description,
				size=size,
				thickness=thickness,
				width=width,
				internal_diameter = internal_diameter,
				description = row[18],
				quantity = quantity,
				unit=row[6],
				value=value,
				tax=tax,
				discount=discount,
				other_expanses=other_expanses,
			)
			print(".",end="")
			# print("." if created else f"{_}\n",end="")
		c+=1
