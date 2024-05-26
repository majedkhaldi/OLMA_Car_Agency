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
    quantity = models.PositiveIntegerField()
    user = models.OneToOneField(User,on_delete= models.CASCADE)
    created_at = models.DateTimeField(auto_now_add =True)
    updated_at = models.DateTimeField(auto_now =True)


class Car(models.Model):
    make = models.CharField(max_length=45)
    model = models.CharField(max_length=45)
    year = models.PositiveIntegerField(max_length=4)
    price = models.FloatField()
    img = models.TextField()
    created_at = models.DateTimeField(auto_now_add =True)
    updated_at = models.DateTimeField(auto_now =True)
    cart = models.ForeignKey(Cart, related_name="cars", on_delete=models.CASCADE, null = True, blank= True)
    users = models.ManyToManyField(User,related_name="cars", null = True, blank= True)
    objects = CarManager() 


class Order(models.Model):
    car = models.ForeignKey(Car,on_delete= models.CASCADE)
    user = models.ForeignKey (User,on_delete= models.CASCADE)
    total_amount = models.PositiveIntegerField()
    date = models.DateField()
    status = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add =True)
    updated_at = models.DateTimeField(auto_now =True)

class Appointment(models.Model):
    user = models.ForeignKey (User,on_delete= models.CASCADE, related_name= 'appointments')
    date = models.DateField()
    status = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add =True)
    updated_at = models.DateTimeField(auto_now =True)

