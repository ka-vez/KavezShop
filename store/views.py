from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from django.db.models import Q
import json
from cart.cart import Cart
# Create your views here.

def search(request):
    #Determine if they filled out the form
    if request.method == 'POST':
        searched = request.POST['searched']
        #query Products databse model
        p_searched =  Product.objects.filter(Q(name__icontains = searched) | Q(description__icontains = searched))
        if not p_searched:
            messages.success(request, 'That Product does not exist' )
            return render(request, 'content/search.html', {})
        else:
            return render(request, 'content/search.html', {'searched' : searched, 'p_searched' : p_searched})
    
    else:
        return render(request, 'content/search.html', {})

def category_summary(request):
    categories = Category.objects.all().order_by('name')
    return render(request, 'content/category_summary.html', {'categories' : categories})

def category(request, cat_egory):
    cat_egory = cat_egory.replace('-', ' ')
    try:
        category = Category.objects.get(name = cat_egory)
        products = Product.objects.filter(category = category)
        return render(request, 'content/category.html', {'products' : products, 'category' : category})
    except:
        messages.success(request, "This category doesn't exist")
        return redirect('home')

def product(request, product_id):
    product = Product.objects.get(id = product_id)
    return render (request,'content/product.html', {'product' : product})

def home(request):
    products = Product.objects.all()
    return render(request, 'content/home.html', {'products': products})

def about(request):
    return render(request, 'content/about.html', {})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)

            #Do some shopping cart stuff
            current_user = Profile.objects.get(user__id = request.user.id)
            #Get their saved cart from database
            saved_cart = current_user.old_cart
            #Convert database string into python dictionary
            if saved_cart:
                #convert to dictionary using json
                converted_cart = json.loads(saved_cart)
                #Add the loaded cart dictionary to our sessiion
                #Get the cart
                cart = Cart(request)
                #Add the items to the cart
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)

            messages.success(request, 'You have been Successfully Logged In')
            return redirect('home')
        else:
            messages.error(request, 'There was an error..... Please try again')
            return redirect('login')
    else:
        return render(request, 'auth/login.html', {})
    
def register_user(request):
    form = SignUpForm
    if request.method  == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            
            user = authenticate(username = username, password = password)
            login(request, user)
            messages.success(request, 'Your Username has been Created, Please fill out your billing info below...')
            return redirect('update-info')
        
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
                return redirect('register')
    else:
        return render(request, 'auth/register.html', {'form' : form})
    
def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id = request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance = current_user)

        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, 'User has been Updated')
            return redirect('home')
        else:
            return render(request, 'auth/update_user.html', {'user_form' : user_form})
    else:
        messages.success(request, 'You must be logged in to access that page!!')
        return redirect('home')
    
def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        # Did they fill out the form
        if request.method  == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            # is the form valid
            if form.is_valid():
                form.save()
                messages.success(request, 'Your Password has been Updated...')
                login(request, current_user)
                return redirect('update-user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update-password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'auth/update_password.html', {'form' : form})
    else:
        messages.success(request, 'You must be logged in to access that page!!')
        return redirect('home')
    
def update_info(request):
    if request.user.is_authenticated:
        #Get current User
        current_user = Profile.objects.get(user__id = request.user.id)
        #Get current user'shipping info
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        #Get original User form
        form = UserInfoForm(request.POST or None, instance = current_user)
        #Get User's Shipping Form
        shipping_form = ShippingForm(request.POST or None, instance = shipping_user)
        if form.is_valid() or shipping_form.is_valid():
            #Save original form
            form.save()
            #save shipping form
            shipping_form.save()
            messages.success(request, 'Your Info has been Updated')
            return redirect('home')
        else:
            return render(request, 'auth/update_info.html', {'form' : form, 'shipping_form' : shipping_form})
    else:
        messages.success(request, 'You must be logged in to access that page!!')
        return redirect('home')

def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out...')
    return redirect('home')

