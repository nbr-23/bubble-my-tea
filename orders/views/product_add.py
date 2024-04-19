from django.views.generic import TemplateView
from orders.models.products import Products  
from django.shortcuts import render
from django.db import connection
from django.shortcuts import redirect
from django.core.files.storage import FileSystemStorage  
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

import os


class ProductAddView(TemplateView):
    template_name = 'product_add.html'
    
    def get(self, request, *args, **kwargs):
        # Check if 'user_id' is in the session
        if 'user_id' not in request.session:
            # Redirect to the login page if the user is not logged in
            return HttpResponseRedirect(reverse_lazy('login'))
        # If 'user_id' exists, retrieve additional information if necessary
        # For example, check the validity of the token or other security checks
        user_id = request.session['user_id']

        # Render page if everything is correct
        return super().get(request, *args, **kwargs)
    
    def post(self, request):
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        picture = request.FILES.get('picture')
        if picture:            
            if picture.content_type.startswith('image'):               
               
                fs = FileSystemStorage(location='orders/static/img/')
                filename = fs.save(picture.name, picture)
                picture_path = os.path.join('img', filename)
            else:
                pass
        else:
            picture_path = None
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO Products (name, description, price, picture) VALUES (%s, %s, %s, %s)", [name, description, price, picture])
        return redirect('/product')