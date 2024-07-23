from store.models import Product
from store.models import Profile
class Cart():
    def __init__(self, request):
        self.session = request.session
        #Get request
        self.request = request

        #Get the current session key
        cart = self.session.get('session_key')

        #If the user i  s new, session key! Create one!
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        #Make sure cart is available on pages on all pages of the website
        self.cart = cart

    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        #Deal with logged in user
        if self.request.user.is_authenticated:
            #Get the current user profile
            current_user = Profile.objects.filter(user__id = self.request.user.id)
            #convert {'3':1, '2':5} to{"3":1, "2":5}
            carty = str(self.cart) 
            carty = carty.replace("\'", "\"")
            #Add the cart to the user profile
            current_user.update(old_cart = carty)


    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        #Deal with logged in user
        if self.request.user.is_authenticated:
            #Get the current user profile
            current_user = Profile.objects.filter(user__id = self.request.user.id)
            #convert {'3':1, '2':5} to{"3":1, "2":5}
            carty = str(self.cart) 
            carty = carty.replace("\'", "\"")
            #Add the cart to the user profile
            current_user.update(old_cart = carty)

    def clear_cart(self):
        cart = self.cart
        cart.clear()     
        self.session.modified = True
        
        #Deal with logged in user
        if self.request.user.is_authenticated:
            #Get the current user profile
            current_user = Profile.objects.filter(user__id = self.request.user.id)
            #convert {'3':1, '2':5} to{"3":1, "2":5}
            carty = str(self.cart) 
            carty = carty.replace("\'", "\"")
            #Add the cart to the user profile
            current_user.update(old_cart = carty)


    def cart_total(self):
        #Get Product IDS
        product_ids = self.cart.keys()
        #lookup those keys in our products database model
        products = Product.objects.filter(id__in=product_ids)
        #Get quantities
        quantites = self.cart
        #Start counting at 0
        total = 0
        for key, value in quantites.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.price * value)
        return total
    
    def __len__(self):
        return len(self.cart)

    def get_prods(self):
        #get ids from cart
        product_ids = self.cart.keys()
        #use ids to lookup products in database model
        products = Product.objects.filter(id__in = product_ids)
        #return the looked up prducts
        return products    

    def get_quants(self):
        quantites = self.cart
        return quantites       

    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)
           
        #get cart
        ourcart = self.cart
        #Update our Dictionary/Cart
        ourcart[product_id] = product_qty

        self.session.modified = True
        
         #Deal with logged in user
        if self.request.user.is_authenticated:
            #Get the current user profile
            current_user = Profile.objects.filter(user__id = self.request.user.id)
            #convert {'3':1, '2':5} to{"3":1, "2":5}
            carty = str(self.cart) 
            carty = carty.replace("\'", "\"")
            #Add the cart to the user profile
            current_user.update(old_cart = carty)
 
        thing = self.cart
        return thing
    
    def delete(self, product):
        product_id = str(product)
        # delte from dictionary/cart

        if product_id in self.cart:
            del self.cart[product_id]
        
        self.session.modified = True

         #Deal with logged in user
        if self.request.user.is_authenticated:
            #Get the current user profile
            current_user = Profile.objects.filter(user__id = self.request.user.id)
            #convert {'3':1, '2':5} to{"3":1, "2":5}
            carty = str(self.cart) 
            carty = carty.replace("\'", "\"")
            #Add the cart to the user profile
            current_user.update(old_cart = carty)








