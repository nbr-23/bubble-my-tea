from django.views.generic import TemplateView
from orders.models.products import Products
from django.shortcuts import redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
import os
from django.db import connection
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from orders.models.users import User 

class ProductUpdateView(TemplateView):
    template_name = 'product_update.html'

 
    def get(self, request, product_id):
        # Vérifie si l'utilisateur est authentifié
        if 'user_id' not in request.session:
            return HttpResponseRedirect(reverse_lazy('login'))
        
        # Vérifie si l'utilisateur est admin
        user_id = request.session['user_id']
        try:
            user = User.objects.get(id=user_id)
            is_admin = user.is_admin
        except User.DoesNotExist:
            is_admin = False
        
        context = {'is_admin': is_admin}

        # Obtient l'objet produit
        product = get_object_or_404(Products, id=product_id)
        context['product'] = product

        return render(request, self.template_name, context)
    
    def post(self, request, product_id):
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        picture = request.FILES.get('picture')

        # Retrieve the product instance for editing
        product = get_object_or_404(Products, id=product_id)

        # Update product details
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
                # Check if the uploaded file is an image
                if picture.content_type.startswith('image'):
                    # Save the uploaded file to the 'img' directory
                    fs = FileSystemStorage(location='orders/static/img/')
                    filename = fs.save(picture.name, picture)
                    picture_path = os.path.join(filename)
                    update_query += "picture = %s, "
                    params.append(picture_path)

            # Remove the trailing comma and space
            update_query = update_query[:-2]

            # Add the WHERE clause
            update_query += " WHERE id = %s"
            params.append(product_id)

            # Execute the update query
            cursor.execute(update_query, params)

        return redirect('/product')
