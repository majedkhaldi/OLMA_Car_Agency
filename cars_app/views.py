from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import User, Order, Cart, Car
from datetime import date
import bcrypt

def index(request):
    return render(request,"index.html")

def register(request):
    if 'userid' in request.session:
        return redirect("index")
    return render(request,"register.html")

def login_page(request):
    if 'userid' in request.session:
        return redirect("index")
    return render(request,"login.html")

def aboutUs(request):
    return render(request, 'about.html')

def contactUs(request):
    if request.method == 'POST':
        username = request.POST.get('usernameCont')
        useremail = request.POST.get('useremail')
        message = request.POST.get('Message')

        if username and useremail and message:
                subject = 'Contact Us Form Submission'
                message_body = f'Name: {username}\nEmail: {useremail}\nMessage: {message}'
                from_email = 'olmaagency4@gmail.com'
                recipient_list = ['olmaagency4@gmail.com']
                send_mail(subject, message_body, from_email, recipient_list, fail_silently=False)
                messages.success(request, 'Thank you for your message. We will get back to you soon.')
                return redirect('ContactUs')
        else:
            messages.error(request, 'All fields are required.')
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
    car =Car.objects.get(id=c_id) 
    return render(request, 'car_details.html', {'car': car})


def shoppingCart(request):
    if 'userid' not in request.session:
        return redirect('Login')
    user = User.objects.get(id=request.session['userid'])
    cart = Cart.objects.get(user=user)
    total_quantity = 0
    if request.method == 'POST':
        for car in cart.cars.all():
            quantity_key = 'quantity_{}'.format(car.id)
            if quantity_key in request.POST:
                quantity = int(request.POST[quantity_key])
                total_quantity += quantity
                cart.total_price += quantity * car.price
    return render(request,'addTocard.html',{'cart': cart, 'total_quantity': total_quantity})

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def update_cart(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.session['userid'])
        cart = Cart.objects.get(user=user)
        
        car_id = request.POST.get('car_id')
        quantity = int(request.POST.get('quantity'))
        
        car = cart.cars.get(id=car_id)
        car_quantity = car.quantity
        
        # Calculate new totals
        total_quantity = 0
        total_price = 0
        
        for car in cart.cars.all():
            if car.id == int(car_id):
                car_quantity = quantity
            total_quantity += car_quantity
            total_price += car_quantity * car.price
        
        # Return updated totals
        data = {
            'total_quantity': total_quantity,
            'total_price': total_price
        }
        return JsonResponse(data)
    return JsonResponse({'error': 'Invalid request'}, status=400)


def addtocart(request, C_id):
    user = User.objects.get(id=request.session['userid'])
    car = Car.objects.get(id=C_id)
    cart = Cart.objects.get(user=user)
    
    if car.inventory > 0:
        cart.cars.add(car)

        
    # carsINcart = cart.cars.all()
    # total_amount = 0
    # for car in carsINcart:
    #     total_amount += car.price

    return redirect('shoppingcart')


def checkout(request):
    if 'userid' not in request.session:
        return redirect('login')
    user = User.objects.get(id=request.session['userid'])
    cart = Cart.objects.get(user=user)
    cars_in_cart = cart.cars.all()
    
    if 'quantity_ordered' not in request.session:
            request.session['quantity_ordered'] = 0
    else:
            for car in cars_in_cart:
                request.session['quantity_ordered'] += 1


    if 'total_amount' not in request.session:
            request.session['total_amount'] = 0
    else:
            for car in cars_in_cart:
                request.session['total_amount'] += car.price

    for car in cars_in_cart:
        Order.objects.create(
            car=car,user=request.user,price=car.price,date=date.today(),status='Pending')
        cart.delete() 
        del request.session['total_amount']
        del request.session['quantity_ordered']
        messages.error(request, 'Your items have been added to the order.\n We will contact you soon.')
        return redirect('chre')


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

