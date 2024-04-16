from django.views.generic import TemplateView
from orders.models.products import Products  
from django.shortcuts import render
from django.db import connection
from django.shortcuts import redirect



class ProductAddView(TemplateView):
    template_name = 'product_add.html'
    
    def post(self, request):
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        picture = request.FILES.get('picture')
        if picture:            
            if picture.content_type.startswith('image'):               
                picture_path = 'orders/static/img' + picture.name
            else:
                pass
        else:
            picture_path = None
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO Products (name, description, price, picture) VALUES (%s, %s, %s, %s)", [name, description, price, picture])
        return redirect('/product')