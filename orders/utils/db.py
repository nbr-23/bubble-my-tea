
try:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'bubbles', 
            'USER': 'root', 
            'PASSWORD': '',  
            'HOST': 'localhost',  
            'PORT': '3306', 
        }
    }
    print("<<< CONNECTED TO THE DATABASE >>>")
except Exception as e:
    print("An error occurred while importing database settings:", e)