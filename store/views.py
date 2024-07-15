from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from .models import Product,Customer,Cart,Order,shipping,Review,Chat,outfit,Professionals,ColourCoding
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.db import connection
from django.db.models import Q
from django.urls import reverse
from .forms import MyOutfit
from django.contrib.auth.decorators import login_required


# Create your views here.
def store(request):
    products=Product.objects.all()
    

    if request.method=="POST":
        product_id=request.POST.get('product_id')
        product=Product.objects.get(id=product_id)

        cart_item_exists = Cart.objects.filter(customer=request.user, product=product)
        if cart_item_exists:
            cart_item = Cart.objects.get(customer=request.user, product=product)
            cart_item.quantity += 1
            cart_item.save()

        else: 
          cart=Cart.objects.create(
            customer=request.user,
            product=product,
            quantity=1,
            )


        # if product is not None:
        #     cart=Cart.objects.get(customer=request.user.customer,product=product)
        #     new_qty=cart.quantity+1
        #     update_cart_quantity(request.user.customer.id, product.id,new_qty)
    product_cart=Cart.objects.filter(customer=request.user.id)


    cart=Cart.objects.filter(customer=request.user.id)
    sum=0
    for prod in cart:
      sum=sum+prod.quantity        


    context={'products':products,'product_cart':product_cart,'cart':sum}
    return render(request,'store.html',context)


@login_required
def cart(request):
    customer=request.user.customer
    items=Cart.objects.filter(customer=request.user.id)
    order=Cart.objects.filter(customer=customer)
    sum1=0
    sum2=0
    subtract=request.GET.get('subtract')
    add=request.GET.get('add')
    
    if add:
        item_id = int(add)
        item = Cart.objects.get(id=item_id, customer=customer)
        item.quantity += 1
        item.save()
        
    
    if subtract:
        item_id=int(subtract)
        item=Cart.objects.get(id=item_id, customer=customer)
        if item.quantity>1:
         item.quantity=item.quantity-1
         item.save()
        else:
            item.delete()


    for od in order:
        sum1=sum1+od.quantity
        sum2=sum2+od.quantity * od.product.price

    context={'items':items,'order':sum1,'total':sum2}
    return render(request,'cart.html',context)

def loginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,'Username does not exist')

        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('store')
        
        else:
            messages.error(request,'username or password incorrect')
    return render(request,'login.html')

def logoutUser(request):
    logout(request)
    return redirect('store')

def registerPage(request):
    form=UserCreationForm

    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            form=UserCreationForm(request.POST)
            user.save()
            login(request,user)
            return redirect('store')
        else:
            messages.error(request,'An error occured')
    context={'form':UserCreationForm}
    return render(request,'register.html',context)


@login_required
def cart(request):
    customer=request.user
    items=Cart.objects.filter(customer=request.user.id)
    order=Cart.objects.filter(customer=request.user.id)
    sum1=0
    sum2=0
    subtract=request.GET.get('subtract')
    add=request.GET.get('add')
    
    if add:
        item_id = int(add)
        item = Cart.objects.get(id=item_id, customer=customer)
        item.quantity += 1
        item.save()
        
    
    if subtract:
        item_id=int(subtract)
        item=Cart.objects.get(id=item_id, customer=customer)
        if item.quantity>1:
         item.quantity=item.quantity-1
         item.save()
        else:
            item.delete()


    for od in order:
        sum1=sum1+od.quantity
        sum2=sum2+od.quantity * od.product.price

    context={'items':items,'order':sum1,'total':sum2}
    return render(request,'cart.html',context)



def checkout(request):
    customer=request.user.id
    order=Cart.objects.filter(customer=customer)
    sum1=0
    sum2=0
    for od in order:
        sum1=sum1+od.quantity
        sum2=sum2+od.quantity * od.product.price
    # order,created=Order.objects.get_or_create(customer=customer,complete=False)
    # items=order.cart_set.all()
    items=Cart.objects.filter(customer=request.user.id)
    context={'items':items,'order':sum1,'total':sum2}
    return render(request,'checkout.html',context)


def product(request,pk):
    product=Product.objects.get(id=pk)
    reviews=Review.objects.filter(product=product)

    if request.method=="POST":
        rev=request.POST.get('review')
        review=Review.objects.create(
            body=rev,
            user=request.user,
            product=product
        )
    context={'product':product,'reviews':reviews}
    return render(request,'product.html',context)


@login_required
def chatting(request):
    users = User.objects.exclude(username=request.user.username)
    sender=request.user
    recipient = None
    chats = []

    if request.method == "POST":
        recipient_username = request.POST.get('recipient')
        recipient = get_object_or_404(User, username=recipient_username)
        Chat.objects.create(
            user=request.user,
            recipient=recipient,
            message=request.POST.get('body')
        )
        return redirect('chatting')  

    if 'recipient' in request.GET:
        recipient_username = request.GET.get('recipient')
        recipient = get_object_or_404(User, username=recipient_username)

    if recipient:
        chats = Chat.objects.filter(
            Q(sender=request.user, recipient=recipient) |
            Q(sender=recipient, recipient=request.user)
        )
    #all_chats = chat.objects.all().order_by('time')
    total=Chat.objects.all()
    context = {
        "messages": chats,
        "users": users,
        "recipient": recipient,
        "total":total,
    }
    return render(request, "chat.html", context)


def websocket(request):
    users=User.objects.all()
    context={'users':users}
    return render(request,'websocket.html',context)


@login_required
def personal(request):
    users = User.objects.exclude(username=request.user.username)
    user=request.user
    recipient = None
    chats = []

    if request.method == "POST":
        recipient_username = request.POST.get('recipient')
        recipient = get_object_or_404(User, username=recipient_username)
        Chat.objects.create(
            user=request.user,
            recipient=recipient,
            message=request.POST.get('body')
        )
        return redirect('personal')  

    if 'recipient' in request.GET:
        recipient_username = request.GET.get('recipient')
        recipient = get_object_or_404(User, username=recipient_username)

    if recipient:
        chats = Chat.objects.filter(
            Q(sender=request.user, recipient=recipient) |
            Q(sender=recipient, recipient=request.user)
        )
    #all_chats = chat.objects.all().order_by('time')
    total=Chat.objects.all()
    context = {
        "messages": chats,
        "users": users,
        "recipient": recipient,
        "total":total,
    }
    return render(request, "chatbox.html", context)
    # recipient=User.objects.get(username=pk)
    # users=User.objects.exclude(username=request.user.username)
    # if request.method=='POST':
    #     chat=Chat.objects.create(
    #         recipient=recipient,
    #         user=request.user,
    #         message=request.POST.get('body')
    #     )
    #     return redirect(reverse('personal', kwargs={'pk': pk}))
    # if recipient:
    #     chats = Chat.objects.filter(
    #         Q(user=request.user, recipient=recipient) |
    #         Q(user=recipient, recipient=request.user)
    #     )
    # total=Chat.objects.all()
    # context={'user':recipient,'total':chats,'messages':chats,'users':users}
    # return render(request,'chatbox.html',context)


def chatPage(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login-user")
    context = {}
    return render(request, "chatPage.html", context)

def colourCoding(request):
    return render(request,'colour.html')



def outfitlist(request):
    users = User.objects.exclude(username=request.user.username)
    user=request.user
    recipient = None
    chats = []
    
    if request.method == "POST":
        recipient_username = request.POST.get('recipient')
        recipient = get_object_or_404(User, username=recipient_username)
        outfit.objects.create(
            user=request.user,
            recipient=recipient,
            message=request.POST.get('body')
        )
        return redirect('outfit')  
    
    if 'recipient' in request.GET:
        recipient_username = request.GET.get('recipient')
        recipient = get_object_or_404(User, username=recipient_username)

    if recipient:
        chats = outfit.objects.filter(
            Q(sender=request.user, recipient=recipient) |
            Q(sender=recipient, recipient=request.user)
        )
    #all_chats = chat.objects.all().order_by('time')
    total=outfit.objects.all()
    context = {
        "messages": chats,
        "users": users,
        "recipient": recipient,
        "total":total,
    }
    return render(request, "outfit.html", context)
    # user=request.user
    # users=User.objects.exclude(username=request.user.username)
    
    # context={'users':users}
    # return render(request,'outfit.html',context)


def fun_outfit(request,pk):
    users=User.objects.exclude(username=request.user.username)
    user=request.user
    recipient=User.objects.get(username=pk)
    products = Product.objects.none() 

    form=MyOutfit()
    if request.method=='POST':
        form=MyOutfit(request.POST,request.FILES)
        print('hello')
        if form.is_valid():
            new_outfit = form.save(commit=False)
            new_outfit.user = user
            new_outfit.message = request.POST.get('message')
            print('hello')
            
            #recipient_message=request.POST.get('message')
            
            new_outfit.recipient = recipient
            new_outfit.save()
            
    recipient_message=outfit.objects.filter(
                Q(user=request.user, recipient=recipient) |
                Q(user=recipient, recipient=request.user)
            ).last()
    if recipient_message:       
     search_terms = recipient_message.message.split() 
     query = Q()  
     for term in search_terms:
                    query |= Q(name__contains=term) | Q(description__contains=term)
                
                
     products = Product.objects.filter(query)
           

                
        
    outfits=outfit.objects.filter(Q(user=request.user, recipient=recipient) |
            Q(user=recipient, recipient=request.user))
    

    
    context={'form':form,'recipient':recipient,'outfits':outfits,'products':products,'msg':recipient_message,'users':users}
    return render(request,'outfitchat.html',context)



def Colour(request,pk):
    colour=ColourCoding.objects.get(skin=pk)
    products=Product.objects.filter(Q(name__icontains=colour.colour1)|Q(name__icontains=colour.colour2)|Q(name__icontains=colour.colour3)|
                                    Q(name__icontains=colour.colour4)|Q(description__icontains=colour.colour1)|Q(description__icontains=colour.colour2)|
                                    Q(description__icontains=colour.colour3)|Q(description__icontains=colour.colour4))
    
    if request.method=="POST":
        product_id=request.POST.get('product_id')
        product=Product.objects.get(id=product_id)

        cart_item_exists = Cart.objects.filter(customer=request.user, product=product)
        if cart_item_exists:
            cart_item = Cart.objects.get(customer=request.user, product=product)
            cart_item.quantity += 1
            cart_item.save()

        else: 
          cart=Cart.objects.create(
            customer=request.user,
            product=product,
            quantity=1,
            )
        
    context={'colours':colour,'products':products}
    return render(request,'colcoding.html',context)


