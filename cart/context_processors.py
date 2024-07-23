from .cart import Cart

# Create context ptocessor so ur cart can work on all pages of the site
def cart(request):
    #Rturn the dfault data from our cart
    return{'cart' : Cart(request)}