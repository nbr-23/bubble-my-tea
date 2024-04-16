from django.views.generic import TemplateView
from orders.models.products import Products
from django.shortcuts import redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
import os
from django.db import connection

class ProductUpdateView(TemplateView):
    template_name = 'product_update.html'
    
    def get(self, request, product_id):
   
        product = get_object_or_404(Products, id=product_id)
        return render(request, self.template_name, {'product': product})
    
    def post(self, request, product_id):
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        picture = request.FILES.get('picture')

       
        product = get_object_or_404(Products, id=product_id)

       
        with connection.cursor() as cursor:
            update_query = "UPDATE Products SET "
            params = []

            if name:
                update_query += "name = %s, "
                params.append(name)

            if description:
                update_query += "description = %s, "
                params.append(description)

            if price:
                update_query += "price = %s, "
                params.append(price)

            if picture:
               
                if picture.content_type.startswith('image'):
                   
                    fs = FileSystemStorage(location='orders/static/img/')
                    filename = fs.save(picture.name, picture)
                    picture_path = os.path.join(filename)
                    update_query += "picture = %s, "
                    params.append(picture_path)

        
            update_query = update_query[:-2] # to remove the ; and space from the end of the query

           
            update_query += " WHERE id = %s"
            params.append(product_id)

          
            cursor.execute(update_query, params)

        return redirect('/product')
