import os 
import webbrowser
os.system("python manage.py makemigrations")
os.system("python manage.py migrate")
webbrowser.open('http://127.0.0.1')
os.system("python manage.py runserver 127.0.0.1:80")
print("after the command✅✅✅✅✅✅")