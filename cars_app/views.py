from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Order ,Cart,Car ,User
from datetime import date
import bcrypt

def index(request):
    return render(request,"login.html")

def AboutUs(request):
    return render(request, 'aboutus.html')

def ContactUs(request):
    if request.method == 'POST':
        username = request.POST.get('usernameCont')
        useremail = request.POST.get('useremail')
        message = request.POST.get('Message')

        if username and useremail and message:
                subject = 'Contact Us Form Submission'
                message_body = f'Name: {username}\nEmail: {useremail}\nMessage: {message}'
                from_email = 'agencyolma@gmail.com'
                recipient_list = ['agencyolma@gmail.com']
                send_mail(subject, message_body, from_email, recipient_list, fail_silently=False)
                messages.success(request, 'Thank you for your message. We will get back to you soon.')
                return redirect('ContactUs')
        else:
            messages.error(request, 'All fields are required.')
    return render(request, 'contact_us.html')



def creat(request):
        
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        messages.error(request, 'Registration failed.')
        return render(request,'login.html', {'errors': errors})
    else:
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        phone_num = request.POST['phone']
        User.objects.create(name=name,email=email,phone_number =phone_num,password=bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode())
        messages.success(request, 'Registration successful. You can now log in.')
        return render(request ,"login.html")

def Login(request):
    email = request.POST.get('emailLog')
    password = request.POST.get('pass')
    user = User.objects.filter(email=email)  
    if user:
        logged_user = user[0] 
        if bcrypt.checkpw(password.encode(), logged_user.password.encode()):
            request.session['userid'] = logged_user.id
            return redirect("cars_page")
        else:
            messages.error(request, 'Incorrect Password')
    else:
        messages.error(request, 'Email not found')
    return redirect('index')

def cars_page(request):
    cars = Car.objects.all()
    makes = Car.objects.values_list('make', flat=True).distinct()
    models = Car.objects.values_list('model', flat=True).distinct()
    colors = Car.objects.values_list('color', flat=True).distinct()

    make_filter = request.GET.get('make')
    model_filter = request.GET.get('model')
    color_filter = request.GET.get('color')
    min_price_filter = request.GET.get('min_price')
    max_price_filter = request.GET.get('max_price')

    if make_filter:
        cars = cars.filter(make=make_filter)
    if model_filter:
        cars = cars.filter(model=model_filter)
    if color_filter:
        cars = cars.filter(color=color_filter)
    if min_price_filter:
        cars = cars.filter(price__gte=min_price_filter)
    if max_price_filter:
        cars = cars.filter(price__lte=max_price_filter)

    data = {
        "usernow" : User.objects.get(id=request.session['userid']),
        "cars" : cars,
        "makes" : makes,
        "models" : models,
        "colors" : colors,
    }

    return render(request,"cars.html",data)



def car_detail(request, C_id):
    car =Car.objects.get(id=C_id) 
    return render(request, 'car_details.html', {'car': car})


def ShoppingCart(request, C_id):
    if 'userid' not in request.session:
        return redirect('login')
    
    user = User.objects.get(id=request.session['userid'])
    car =Car.objects.get(id=C_id) 
    cart = Cart.objects.get(car=car, user=user)
    return render(request, 'shoppingCart.html', {'cart': cart})


def checkout(request):
    if 'userid' not in request.session:
        return redirect('login')
    cart = Cart.objects.get(user=request.user)
    cars_in_cart = cart.cars.all()
    total_amount = sum(car.price for car in cars_in_cart)

    for car in cars_in_cart:
        Order.objects.create(
            car=car,
            user=request.user,
            total_amount=total_amount,
            date=date.today(),
            status='Pending'
        )
        car.cart = None
        car.save()

    cart.delete() 
    return HttpResponse(request,'Your items have been added to the order.\n We will contact you soon.')  # Redirect to a success page or order summary


def FAQS(request):
    return render(request, 'faqs.html')
