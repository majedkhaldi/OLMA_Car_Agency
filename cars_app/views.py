
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User,Car,Cart,Appointment,Order
import bcrypt

def index(request):
    return render(request,"index.html")

def login_page(request):
    if "userid" in request.eseeion:
        return redirect('/cars')
    return render(request,"login.html")

def register_page(request):
    if "userid" in request.eseeion:
        return redirect('/cars')
    return render(request,"register.html")

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        phone_number = request.POST['phone_number']
        logged_user = User.objects.create(name = name, email = email, phone_number = phone_number, password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode())
        request.session['userid'] = logged_user.id
        return redirect('/cars')

def login(request):
    user = User.objects.filter(email = request.POST['loginemail'])
    if user: 
        logged_user = user[0] 
        if bcrypt.checkpw(request.POST['loginpassword'].encode(), logged_user.password.encode()):
            request.session['userid'] = logged_user.id
            return redirect('/cars')
    else:
        messages.error(request,'this email cannot be found', extra_tags= 'emailnotfound')
        return redirect('/')
        
def cars_page(request):

    data = {
        "usernow" : User.objects.get(id=request.session['userid']),
        "cars" : Car.objects.all()
    }
    return render(request,"cars.html",data)

def logout(request):
    del request.session['userid']
    return redirect ('/')



# Create your views here.

# Create your views here.
