
try:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'bubbles', 
            'USER': 'root', 
            'PASSWORD': 'Janvier9.@',  
            'HOST': 'localhost',  
            'PORT': '3306', 
            'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
        }
    }
    print("<<< CONNECTED TO THE DATABASE >>>")
except Exception as e:
    print("An error occurred while importing database settings:", e)