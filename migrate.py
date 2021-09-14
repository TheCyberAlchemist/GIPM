import os 
import webbrowser
os.system("python manage.py makemigrations")
os.system("python manage.py migrate")
print("after the migrations ✅✅✅✅✅")