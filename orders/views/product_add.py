from django.views.generic import TemplateView
from orders.models.products import Products  
from django.shortcuts import render
from django.db import connection
from django.shortcuts import redirect
from django.core.files.storage import FileSystemStorage  
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from orders.models.users import User 
import os


class ProductAddView(TemplateView):
    template_name = 'product_add.html'
    
    def get(self, request, *args, **kwargs):
        # Check if 'user_id' is in the session
        if 'user_id' not in request.session:
            # Redirect to the login page if the user is not logged in
            return HttpResponseRedirect(reverse_lazy('login'))
       
        user_id = request.session['user_id']
        
        try:
            user = User.objects.get(id=user_id)
            is_admin = user.is_admin
        except User.DoesNotExist:
            is_admin = False
        
        context = {
        'is_admin': is_admin
        }

       
        return super().get(request, *args, **kwargs, **context)
    
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