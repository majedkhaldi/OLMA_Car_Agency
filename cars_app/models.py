from django.db import models
import re

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    
            errors['email'] = "Invalid email address!"
        if len(postData['name']) <= 1 :
            errors["name"] = "Your name should be at least 2 characters"
        if len(postData['password']) < 8 :
            errors["password"] = "Password should be at least 8 characters"
        if postData['password'] != postData['cpassword'] :
            errors["cpassword"] = "Password did not match"
        return errors
    
class CarManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['make']) <= 1 :
            errors["make"] = "Make should be at least 2 characters"
        if len(postData['model']) <= 1 :
            errors["model"] = "Model should be at least 2 characters"
        if len(postData['year']) != 4 or postData['year'] < 0:
            errors["year"] = "Please enter a valid year (YYYY)"
        if len(postData['price']) == 0 or postData['price'] < 0 :
            errors["price"] = "Please enter a valid price"
        return errors

class User(models.Model):
    name = models.CharField(max_length=45)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add =True)
    updated_at = models.DateTimeField(auto_now =True)
    objects = UserManager() 



class Cart(models.Model):
    total_price = models.PositiveIntegerField(default=0)
    user = models.OneToOneField(User,on_delete= models.CASCADE)
    created_at = models.DateTimeField(auto_now_add =True)
    updated_at = models.DateTimeField(auto_now =True)


class Car(models.Model):
    make = models.CharField(max_length=45)
    model = models.CharField(max_length=45)
    year = models.PositiveIntegerField()
    price = models.FloatField()
    img = models.TextField()
    color = models.CharField(max_length=45)
    inventory = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add =True)
    updated_at = models.DateTimeField(auto_now =True)
    carts = models.ManyToManyField(Cart, related_name="cars", blank= True)
    users = models.ManyToManyField(User,related_name="cars", blank= True)
    objects = CarManager() 


class Order(models.Model):
<<<<<<< HEAD
    STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
    ]
=======
>>>>>>> master
    cars = models.ManyToManyField(Car,related_name='orders')
    user = models.ForeignKey (User,on_delete= models.CASCADE)
    total_amount = models.PositiveIntegerField()
    total_price = models.PositiveIntegerField()
<<<<<<< HEAD
    status = models.CharField(max_length=45, choices=STATUS_CHOICES)
=======
    status = models.CharField(max_length=45)
>>>>>>> master
    created_at = models.DateTimeField(auto_now_add =True)
    updated_at = models.DateTimeField(auto_now =True)

class Appointment(models.Model):
    user = models.ForeignKey (User,on_delete= models.CASCADE, related_name= 'appointments')
    date = models.DateField(null=True)
    status = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add =True)
    updated_at = models.DateTimeField(auto_now =True)

<<<<<<< HEAD
class CarImage(models.Model):
    car = models.ForeignKey(Car, related_name='images', on_delete=models.CASCADE)
    image_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add =True)
    updated_at = models.DateTimeField(auto_now =True)
=======
>>>>>>> master

class Messages(models.Model):
    message=models.TextField(max_length=45)
    user = models.ForeignKey(User, related_name='messages',on_delete=models.CASCADE,null=True)
<<<<<<< HEAD
    car = models.ForeignKey(Car, related_name='messages',on_delete=models.CASCADE,null=True)
=======
>>>>>>> master
    created_at = models.DateTimeField(auto_now_add = True,null=True)
    updated_at = models.DateTimeField(auto_now = True)

class Comments(models.Model):
    comment=models.TextField(max_length=45)
    user = models.ForeignKey(User,related_name='comments' ,on_delete=models.CASCADE,null=True)
    message = models.ForeignKey(Messages, related_name='comments',on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(auto_now_add = True,null=True)
    updated_at = models.DateTimeField(auto_now = True)
<<<<<<< HEAD
=======


>>>>>>> master
