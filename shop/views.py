from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Product, Contact, Orders, OrderUpdate
from math import ceil
import json

# Extra Features
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout



# Create your views here.



def index(request):
    # products = Product.objects.all()
    # print(products)
    # n = len(products)
    # nSlides = n // 4 + ceil((n / 4) - (n // 4))

    allProds=[]
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}                                       # Set comprehension
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])



    # params = {'no_of_slides': nSlides, 'range': range(1, nSlides), 'product': products}
    # allProds = [[products, range(1, nSlides), nSlides],
    #             [products, range(1, nSlides), nSlides]]
    params = {'allProds': allProds}
    # print(params)

    return render(request, 'shop/index.html', params)





def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    thank = False
    if request.method=="POST":
        print(request)
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        # thank = True
        # print(name, email, phone, desc)

        if len(name)<2 or len(email)<2 or len(phone)<2 or len(desc)<2:
            messages.error(request, "Please fill the form correctly!")
        else:
            contact = Contact(name=name, email=email, phone=phone, desc=desc)
            contact.save()
            messages.success(request, "Your details has been registered successfully!")
    # return render(request, 'shop/contact.html', {'thank': thank})
    return render(request, 'shop/contact.html')


def search(request):
    return render(request, 'shop/search.html')

def productView(request, myid):
    # Fetch the product using the id
    product = Product.objects.filter(id=myid)
    print(product)
    print(product[0])

    return render(request, 'shop/prodView.html', {'product': product[0]})

def checkout(request):
    if request.method == "POST":
        print(request)
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')

        # print(name, email, phone, desc)
        order = Orders(items_json=items_json , name=name, email=email, address=address, city=city, state=state, zip_code=zip_code, phone=phone)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id                                                                         # To get id of the order, that is displayed in alert box and helps to track orders

        return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})                    # 'thank' --> new parameter, : thank --> already declared variable
    return render(request, 'shop/checkout.html')


def tracker(request):

    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        # return HttpResponse(f"{orderId} and {email}")           # Used for testing
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps([updates,order[0].items_json], default=str)
                return HttpResponse(response)                                       # Very important to keep this line of code outside the for loop. If indented, it goes inside it, and will only show first update, that is of placing the order.
            else:
                return HttpResponse('{}')
        except Exception as e:
            # return HttpResponse(f'Exeptions  {e}')
            return HttpResponse('{}')


    return render(request, 'shop/tacker.html')




def samplenew(request):
    return render(request, 'shop/samplenew.html')




def handleSignup(request):
    if request.method == 'POST':
        # Get Post Parameters
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # Check for errorness
        # Username should have less than 10 characters
        if len(username)>20:
            messages.error(request, "Username must be less than 10 characters.")
            return redirect('ShopHome')
        #  Username should be alphanum
        if not username.isalnum():
            messages.error(request, "Username must only contain alphabet or characters.")
            return redirect('ShopHome')
        # Passwords should match
        if pass1 != pass2:
            messages.error(request, "Passwords don't match.")
            return redirect('ShopHome')
            
        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your SHOPHUNT account has been successfully created!")
        return redirect('ShopHome')
    else:
        return HttpResponse("404 - Not Found")  


def handleLogin(request):
    if request.method == 'POST':
        # Get the post parameters
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']
        

        user = authenticate(username=loginusername, password=loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in")
            return redirect('ShopHome')
        else:
            messages.error(request, "Invalid credentials. Please Try Again.")
            return redirect('ShopHome')


    return HttpResponse("404 - Not Found")






def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('ShopHome')