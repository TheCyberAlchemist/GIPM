import sys
# sys.path.append("C:\\Users\\admin\\Desktop\\Somewhere\\dad")
import csv
from .models import *
with open("C:\\Users\\admin\\Desktop\\Somewhere\\dad\\CSV\\VENDOR DETAIL.csv") as f:
	reader = csv.reader(f)
	c = 0
	for row in reader:
		# if not row[0]:
		# print(row)
		if c != 0:
			_, created =  vendor_details.objects.get_or_create(
				vendor_name=row[0],
				address=row[1],
				contact_person=row[2],
				contact_number=row[3],
				email=row[4],
				gst_no=row[5],
				name_of_bank=row[6],
				acc_no=row[7],
				ifsc_code=row[8],
				branch=row[9],
			)
			print(".",end="")
		c+=1