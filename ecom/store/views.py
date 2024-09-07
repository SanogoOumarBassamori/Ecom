from django.shortcuts import render, redirect
from .models import Product, Category,Profile
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserform,ChangePasswordForm, UserInfoForm

from payement.forms import ShippingForm
from payement.models import ShippingAddress

from django import forms
from django.db.models import Q
import json
from cart.cart import Cart

# Create your views here.

def search(request):
    if request.method == "POST":
        searched = request.POST['searched']

        searched = Product.objects.filter(Q(name__icontains= searched) | Q(description__icontains= searched))
        if not searched:
            messages.success(request, "Desoler ce produit n'est pas disponible...")
            return render(request, 'search.html', {})
        else:
            return render(request, 'search.html', {"searched":searched})
    else:
        return render(request, 'search.html', {})

def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)

        form = UserInfoForm(request.POST or None, instance=current_user)

        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        if form.is_valid() or shipping_form.is_valid():
            form.save()

            shipping_form.save()

            messages.success(request, "Vos Info ont été Modifier !!")
            return redirect('home')
        return render(request, 'update_info.html', {"form":form, 'shipping_form':shipping_form})
    else:
        messages.success(request, "Vous devez etre connecté pour avoir accès !!")
        return redirect('home')

def update_password(request):

    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "votre Mot de passe a été Modifier!!, Veuillez vous reconnecter...")
                #login(request, current_user)
                return redirect('login')
            else :
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')

            
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {"form":form})
    else:
        messages.success(request, "Vous devez etre connecté pour avoir accès !!")
        return redirect('home')
def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserform(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, "L'utilisateur a été Modifier !!")
            return redirect('home')
        return render(request, 'update_user.html', {"user_form":user_form})
    else:
        messages.success(request, "Vous devez etre connecté pour avoir accès !!")
        return redirect('home')

def cart_summary(request):
    categories = Category.objects.all()
    return render(request, 'cart_summary.html', {"categories":categories})

def category(request,foo):
    foo = foo.replace('-', ' ')

    try:
        category= Category.objects.get(name=foo)
        products= Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':products, 'category':category})
    except:
        messages.success(request, ("Oups cette categorie n'existe pas...!"))
        return redirect('home')    

def product(request,pk):
    product= Product.objects.get(id=pk)
    return render(request, 'product.html', {'product':product})

def home(request):
    products= Product.objects.all()
    return render(request, 'home.html', {'products':products})

def about(request):
    
    return render(request, 'about.html', {})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user =  authenticate(request, username=username,password=password)
        if user != None:
            login(request,user)

            current_user = Profile.objects.get(user__id=request.user.id)

            saved_cart = current_user.old_cart

            if saved_cart:
                converted_cart = json.loads(saved_cart)
                cart = Cart(request)
                for key,value in converted_cart.items():
                    cart.db_add(product=key,quantity=value)

            messages.success(request, ("Vous etes connecté avec Succes!!"))
            return redirect('home')
        else:    
            messages.success(request, ("Erreur de connection veuillez réessayer!!"))
            return redirect('login')
    else:
        return render(request, 'login.html', {})
    

def logout_user(request):
    logout(request)
    messages.success(request, ("Vous avez été déconnecté.... Merci!"))
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
       
        if form.is_valid():
            
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user =  authenticate(username=username , password=password)
            login(request, user)
            messages.success(request, ("Vous etes Enregistrez avec Succes!!"))
            return redirect('update_info')
        else:
            messages.success(request, ("Oups un problème est survenu veuillez réessayer SVP!!"))
            return redirect('register')
        
    else:    


     return render(request, 'register.html', {'form':form})