from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib import messages
from store.models import Product, Profile
import datetime

# Create your views here.
def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        order = Order.objects.get(id=pk)
        order_item = OrderItem.objects.filter(order_id = pk)

        if request.POST:
            status = request.POST['shipping_status']
            #check if true or false
            if status == 'True':
                #Get the order
                order = Order.objects.filter(id=pk)
                #get the status
                now = datetime.datetime.now()
                order.update(shipped = True, date_shipped = now )
            
            else:
                #Get the order  
                order = Order.objects.filter(id=pk)
                #get the status
                order.update(shipped = False)
            messages.success(request, 'Shipping Status Updated')
            return redirect('home')




        return render(request, 'payment/order_item.html', {'order' : order, 'order_item' : order_item})
    
    else:
        messages.success(request, 'Access Denied')
        return redirect('home')


def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)
        return render(request, 'payment/not-shipped-dash.html', {'orders' : orders})
    
    else:
        messages.success(request, 'Access Denied')
        return redirect('home')
def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        return render(request, 'payment/shipped-dash.html', {'orders' : orders})
    
    else:
        messages.success(request, 'Access Denied')
        return redirect('home')

def process_order(request):
    if request.POST:
        #Get Cart
        cart = Cart(request)
        cart_products =  cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        #Get billing form from last page
        payment_form = (request.POST or None)
        #Get shipping session data
        my_shipping = request.session.get('my_shipping')
        
        #Gather Order Info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        amount_paid = totals
        #create shipping address from session info
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zip_code']}\n{my_shipping['shipping_country']}\n"
        
        #Create an order
        if request.user.is_authenticated:
            #logged in
            user = request.user
            #create order
            create_order = Order(user = user, full_name = full_name, email = email, Shipping_address = shipping_address, amount_paid = amount_paid)
            create_order.save()

            #Add order items
            #Get the order ID
            order_id = create_order.id
            #Get product stuff
            for product in cart_products():
                #Get product ID
                product_id = product.id
                #Get product price
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                #Get quantity
                for key, value in quantities().items():
                    if int(key) == product_id:
                        #Create order item
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quantity=value, price=price)
                        create_order_item.save() 

            #Delete our cart
            for key in list(request.session.keys()):
                #delete the key
                if key == "session_key":
                    del request.session[key]

            #Delete the cart from the database
            current_user = Profile.objects.filter(user__id = request.user.id)
            #Delete shopping cart in the database
            current_user.update(old_cart = "")


            messages.success(request, 'Order Placed')
            return redirect('home')

        else:
            create_order = Order(full_name = full_name, email = email, Shipping_address = shipping_address, amount_paid = amount_paid)
            create_order.save()

            #Add order items
            #Get the order ID
            order_id = create_order.id
            #Get product stuff
            for product in cart_products():
                #Get product ID
                product_id = product.id
                #Get product price
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                #Get quantity
                for key, value in quantities().items():
                    if int(key) == product_id:
                        #Create order item
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=value, price=price)
                        create_order_item.save() 

            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]


            messages.success(request, 'Order Placed')
            return redirect('home')
        
    else:
        messages.success(request, 'Access Denied')
        return redirect('home')
        

def billing_info(request):
    if request.POST:
        cart = Cart(request)
        cart_products =  cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        #Check if user is logged in
        if request.user.is_authenticated:
            #Get Billing Form
            billing_form = PaymentForm()
            return render(request, 'payment/billing-info.html', {'cart_products' : cart_products, 'quantities' : quantities, 'totals' : totals, 'shipping_info' : request.POST, 'billing_form' :billing_form })
        
        #Not logged in
        else:
            #Get Billing Form
            billing_form = PaymentForm()
            return render(request, 'payment/billing-info.html', {'cart_products' : cart_products, 'quantities' : quantities, 'totals' : totals, 'shipping_info' : request.POST, 'billing_form' : billing_form })

    else:
        messages.success(request, 'Access Denied')
        return redirect('home')


def checkout(request):
    cart = Cart(request)
    cart_products =  cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total

    #Check out as guest
    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance = shipping_user)
        return render(request, 'payment/checkout.html', {'cart_products' : cart_products, 'quantities' : quantities, 'totals' : totals, 'shipping_form' : shipping_form })
    
    #Check out as logged in user
    else:
        shipping_form = ShippingForm(request.POST or None)
        return render(request, 'payment/checkout.html', {'cart_products' : cart_products, 'quantities' : quantities, 'totals' : totals, 'shipping_form' : shipping_form})

def payment_success(request):
    return render(request, 'payment/payment_success.html', {})
