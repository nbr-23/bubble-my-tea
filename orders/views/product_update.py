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
        # Récupère les données du formulaire
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        picture = request.FILES.get('picture')

        # Obtient l'objet produit
        product = get_object_or_404(Products, id=product_id)

        # Met à jour les champs du produit
        if name:
            product.name = name
        if description:
            product.description = description
        if price:
            product.price = price
        if picture:
            product.picture = picture

        # Enregistre les modifications dans la base de données
        product.save()

        # Redirige vers la page de liste des produits
        return redirect('/product')
