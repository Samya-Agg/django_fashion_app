from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=200,null=True,blank=True)
    email=models.EmailField(max_length=200,null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name=models.CharField(max_length=200,null=True)
    price=models.FloatField()
    description=models.TextField(max_length=1000,null=True,blank=False)
    image=models.ImageField(null=True,blank=True,default='placeholder.png')


    def __str__(self):
        return self.name
    
class Order(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    date_ordered=models.DateTimeField(auto_now_add=True)
    complete=models.BooleanField(default=False,blank=True,null=True)
    transaction_id=models.CharField(max_length=200,null=True)

    def __str__(self):
        return str(self.id)
    
    # @property
    # def get_total(self):
    #     cart=self.cart_set.all()
    #     total=sum([item.get_sum for item in cart])
    #     return total
    

    # @property
    # def get_qty(self):
    #     cart=self.cart_set.all()
    #     total=sum([item.quantity for item in cart])
    #     return total

class Cart(models.Model):
    customer=models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,blank=True,null=True)
    quantity=models.IntegerField(default=0,null=True,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)


    @property
    def get_sum(self):
        total=self.quantity * self.product.price
        return total
    
    @property
    def get_total(self):
        cart=self.objects.all()
        total=sum([item.get_sum for item in cart])
        return total
    

    @property
    def get_qty(self):
        cart=self.objects.all()
        total=sum([item.quantity for item in cart])
        return total

class shipping(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    address=models.CharField(max_length=200,null=True)
    city=models.CharField(max_length=200,null=True)
    state=models.CharField(max_length=200,null=True)
    zipcode=models.CharField(max_length=200,null=True)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
    

class Review(models.Model):
     user=models.ForeignKey(User,on_delete=models.CASCADE)
     product=models.ForeignKey(Product,on_delete=models.CASCADE)
     body=models.TextField()
     updated=models.DateTimeField(auto_now=True)
     created=models.DateTimeField(auto_now_add=True)

     def __str__(self):
         return self.body[0:50]


class Chat(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=False,blank=False)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message=models.TextField(max_length=500)
    time=models.DateTimeField(auto_now=True)


class ColourCoding(models.Model):
    skin=models.TextField(max_length=100)
    colour1=models.TextField(max_length=100)
    colour2=models.TextField(max_length=100)
    colour3=models.TextField(max_length=100)
    colour4=models.TextField(max_length=100)
    



class Professionals(models.Model):
    name=models.TextField(max_length=50)
    username=models.TextField(max_length=100,unique=True,null=False)
    description=models.TextField(max_length=200)

class outfit(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    message=models.TextField(max_length=200)
    image=models.ImageField(null=True,upload_to="")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE,related_name='received_outfits')



