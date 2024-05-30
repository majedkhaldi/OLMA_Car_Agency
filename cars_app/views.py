from django.core.mail import send_mail
from django.shortcuts import render, redirect ,get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import User, Order, Cart, Car, Messages,Comments
from datetime import date
import bcrypt
from django.template.loader import render_to_string
from django.conf import settings
from django.http import JsonResponse
from django.db.models import Q
from django.db.models import Sum

def index(request):
    if 'visitorcounter' not in request.session:
        request.session['visitorcounter'] = 1000
    else:
        request.session['visitorcounter'] += 1
    return render(request,"index.html")

def register(request):
    if 'userid' in request.session:
        return redirect("index")
    return render(request,"register.html")

def login_page(request):
    if 'userid' in request.session:
        return redirect("index")
    return render(request,"login.html")

from django.db.models import Sum

def aboutUs(request):
    # Calculate total sales
    sales = Order.objects.filter(status='completed')
    print(sales)
    # Ensure 'visitorcounter' exists in the session
    number_of_visitors = request.session.get('visitorcounter', 0)
    total_price = 0
    for sale in sales:
        total_price += sale.total_price
        print(total_price)
    # Prepare data for the template
    data = {
        "numberofvisitors": number_of_visitors,
        "total_price": (total_price/1000000)
    }
    
    return render(request, 'about.html', data)


def contactUs(request):
    if request.method == 'POST':
        username = request.POST.get('usernameCont')
        useremail = request.POST.get('useremail')
        message = request.POST.get('Message')
        if username and useremail and message:
            subject = 'Contact Us Form Submission'
            context = {'username': username, 'useremail': useremail, 'message': message}
            message_body = render_to_string('contact_email_template.html', context)
            from_email = settings.EMAIL_HOST_USER
            recipient_list = ['agencyolma@gmail.com']
            send_mail(subject, message_body, from_email, recipient_list, fail_silently=False, html_message=message_body)
            messages.success(request, 'Thank you for your message. We will get back to you soon.')
            return redirect('ContactUs')
        else:
            messages.error(request, 'All fields are required.')
    else:
        if 'flag' in request.session:
            messages.success(request, 'Please contact us to place an order for this car',extra_tags= "soldout")
        else:
            return render(request, 'contact.html')
    del request.session['flag']
    return render(request, 'contact.html')



def create(request):

    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for name, value in errors.items():
            messages.error(request, value, extra_tags= 'nameerror')
        for email, value in errors.items():
            messages.error(request, value, extra_tags= 'emailerror')
        for pnumber, value in errors.items():
            messages.error(request, value, extra_tags= 'phoneerror')
        for password, value in errors.items():
            messages.error(request, value, extra_tags= 'passworderror')
        for cpassword, value in errors.items():
            messages.error(request, value, extra_tags= 'cpassworderror')
        return redirect('/registerpage')
    else:
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        phone_num = request.POST['pnumber']
        logged_user = User.objects.create(name=name,email=email,phone_number =phone_num,password=bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode())
        request.session['userid'] = logged_user.id
        Cart.objects.create(user= logged_user)
        return redirect("index")

def login(request):
    email = request.POST.get('emailLog')
    password = request.POST.get('pass')
    user = User.objects.filter(email=email)  
    if user:
        logged_user = user[0] 
        if bcrypt.checkpw(password.encode(), logged_user.password.encode()):
            request.session['userid'] = logged_user.id
            return redirect("cars_page")
        else:
            messages.error(request, 'Incorrect Password', extra_tags= 'emailnotfound')
    else:
        messages.error(request, 'Email not found', extra_tags= 'incorrectpass')
    return redirect('/loginpage')

def cars_page(request):
    cars = Car.objects.all()
    makes = Car.objects.values_list('make', flat=True).distinct()
    models = Car.objects.values_list('model', flat=True).distinct()
    colors = Car.objects.values_list('color', flat=True).distinct()
    years = Car.objects.values_list('year', flat=True).distinct()

    make_filter = request.GET.get('make')
    model_filter = request.GET.get('model')
    color_filter = request.GET.get('color')
    year_filter = request.GET.get('year_from')
    min_price_filter = request.GET.get('min_price')
    max_price_filter = request.GET.get('max_price')

    if make_filter:
        cars = cars.filter(make=make_filter)
    if model_filter:
        cars = cars.filter(model=model_filter)
    if color_filter:
        cars = cars.filter(color=color_filter)
    if year_filter:
        cars = cars.filter(year=year_filter)
    if min_price_filter:
        cars = cars.filter(price__gte=min_price_filter)
    if max_price_filter:
        cars = cars.filter(price__lte=max_price_filter)

    data = {
        # "usernow" : User.objects.get(id=request.session['userid']),
        "cars" : cars,
        "makes" : makes,
        "models" : models,
        "colors" : colors,
        "years" : years,
    }

    return render(request,"cars.html",data)

def car_detail(request, c_id):
    car = Car.objects.get(id=c_id)
    data = {
        'car' : Car.objects.get(id=c_id), 
        'message' : Messages.objects.filter(car = car),
    } 
    return render(request, 'car_details.html', data)

def shoppingCart(request):
    if 'userid' not in request.session:
        return redirect('Login')
    
    user = User.objects.get(id=request.session['userid'])
    cart = Cart.objects.get(user=user)
    total_quantity = 0
    total_price = 0


    for car in cart.cars.all():
        total_price += car.price
        total_quantity += 1


            # Update cart total price and total quantity
    # cart.total_price = total_price
    # request.session['total_quantity'] = total_quantity
    # cart.save()

    return render(request, 'addTocard.html', {'cart': cart, 'total_quantity': total_quantity, 'total_price': total_price})


# def shoppingCart(request):
#     if 'userid' not in request.session:
#         return redirect('Login')
    
#     user = User.objects.get(id=request.session['userid'])
#     cart = Cart.objects.get(user=user)
    
#     request.session['total_quantity'] = 0
#     total_price = 0
    
#     for car in cart.cars.all():
#         quantity_key = 'quantity_{}'.format(car.id)
#         print(request.POST)
#         if quantity_key in request.POST:
#             quantity = int(request.POST[quantity_key])
#             request.session['total_quantity'] += quantity
#             total_price += (quantity * car.price)

#     # Update session with total quantity
#     # request.session['total_quantity'] = request.session['total_quantity']
#     cart.total_price = total_price

#     cart.save()
    
#     return render(request, 'addTocard.html', {'cart':cart,'total_quantity': request.session['total_quantity'], 'total_price': total_price})



# def shoppingCart(request):
#     if 'userid' not in request.session:
#         return redirect('Login')
#     user = User.objects.get(id=request.session['userid'])
#     cart = Cart.objects.get(user=user)
#     if 'total_quantity' not in request.session:
#         request.session['total_quantity'] = 0

#     # if request.method == 'POST':
#     for car in cart.cars.all():
#         quantity_key = 'quantity_{}'.format(car.id)
#         if quantity_key in request.POST:
#             quantity = int(request.POST[quantity_key])
#             request.session['total_quantity'] += quantity
#             cart.total_price += (quantity * car.price)
    
#     # print(quantity)

#     return render(request,'addTocard.html',{'cart': cart, 'total_quantity': request.session['total_quantity']})


def addtocart(request, C_id):
    if 'userid' not in request.session:
        return redirect('Login')
    user = User.objects.get(id=request.session['userid'])
    car = Car.objects.get(id=C_id)
    cart = Cart.objects.get(user=user)
    
    if car.inventory > 0:
        cart.cars.add(car)

        
    # carsINcart = cart.cars.all()
    # total_amount = 0
    # for car in carsINcart:
    #     total_amount += car.price

    return redirect('/process')


def checkout(request):
    if 'userid' not in request.session:
        return redirect('login')
    
    user = User.objects.get(id=request.session['userid'])
    cart = Cart.objects.get(user=user)
    cars_in_cart = cart.cars.all()
    
    total_quantity = 0
    total_price = 0.0

    if request.method == 'POST':
        for car in cars_in_cart:
            car_id = str(car.id)
            if car_id in request.POST:
                quantity = int(request.POST[car_id])
                total_quantity += quantity
                total_price += (quantity * car.price)
                car.inventory -= quantity

    this_order = Order.objects.create(user=user, total_amount=total_quantity, total_price=total_price, status='pending')
    for car in cars_in_cart:
        this_order.cars.add(car)

    cart.cars.clear() 
    cart.total_quantity = 0
    cart.total_price = 0.0
    cart.save()

    messages.success(request, 'Your items have been added to the order. We will contact you soon.')
    return redirect('shoppingcart')



def chre(request):
    quantity_ordered = request.session.get('quantity_ordered')
    total_price = request.session.get('total_price')

    context = {
        'quantity_ordered': quantity_ordered,
        'total_price': total_price,
    }
    return render(request, "checkout.html", context)


def fAQS(request):
    return render(request, 'faqs.html')

def logout(request):
    del request.session['userid']
    return redirect('/loginpage')

def search_cars(request):
    if request.method == 'GET':
        query = request.GET.get('q', '')
        if query:
            cars = Car.objects.filter(Q(make__icontains=query) | Q(model__icontains=query))
        else:
            cars = Car.objects.none() 
        car_list = list(cars.values('id', 'make', 'model', 'year', 'price', 'img', 'color'))
        return JsonResponse(car_list, safe=False)
    
def all_cars(request):
    cars = Car.objects.all()
    cars_list = list(cars.values('id', 'make', 'model', 'year', 'price', 'img'))
    return JsonResponse(cars_list, safe=False)
    

def removeitem(request,c_id):
    user = User.objects.get(id=request.session['userid'])
    cart = Cart.objects.get(user=user)
    this_car = Car.objects.get(id = c_id)
    cart.cars.remove(this_car)
    return redirect('/cart')

def soldout (request):
    if 'flag' not in request.session:
        request.session['flag'] = 1
    return redirect ('ContactUs')

def addmessage(request,c_id):
    if 'userid' not in request.session:
        return redirect ('LoginPage')
    message=request.POST['reviewmessage']
    user=User.objects.get(id=request.session['userid'])
    car=Car.objects.get(id=c_id)
    Messages.objects.create(message=message,user=user, car = car)
    return redirect('details',c_id)
    # data={
    #     'messages':Messages.objects.all()
    # }
    # return render(request,'car_details.html',data)


# def create_message(request,c_id):

#     message=request.POST['message']
#     car=Car.objects.get(id=c_id)
#     user=User.objects.get(id=request.session['userid'])
#     Messages.objects.create(message=message,user=user)
#     return redirect('/review')

def addcomment(request,c_id,m_id):
    if 'userid' not in request.session:
        return redirect ('LoginPage')
    comment=request.POST['reviewcomment']
    user=User.objects.get(id=request.session['userid'])
    messages=Messages.objects.get(id=m_id)
    Comments.objects.create(comment=comment,user=user,message=messages)
    return redirect('details',c_id)