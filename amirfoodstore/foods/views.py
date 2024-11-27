from django.shortcuts import render,redirect
from .models import Food,Category


from django.db.models import Q
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

import json

from cart.cart import Cart
# from shop.forms import ProfileRegisterForm


def search(request):
    if request.method=='POST':
        searched = request.POST['searched']
        searched = Food.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        if not searched:
            messages.success(request,"not found")
            return render(request,'shop/search.html',{})
        else:
            return render(request,'shop/search.html',{'searched':searched})


    else:

        return render(request,'shop/search.html',{})



def index(request):
    products = Food.objects.all()
    return render(request, 'shop/index.html', {'products': products})


def product(request,pk):

    product = Food.objects.get(id=pk)
    return render(request,"shop/detail.html",{'product':product})



def category(request,cat):
    cat=cat.replace("-"," ")
    try:
        category=Category.objects.get(name=cat)
        products=Food.objects.filter(category=category)
        return render(request,"shop/category.html",{"products":products,"category":category})

    except:
        products=Food.objects.filter(category=cat)
        messages.success(request, ('error'))
        return redirect("home")


def category_summary(request):
    all_cat = Category.objects.all()
    return render(request, 'shop/category_summary.html', {'category':all_cat})





