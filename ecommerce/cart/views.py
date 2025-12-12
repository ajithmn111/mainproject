from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from shop.models import Product
from cart.models import Cart
import razorpay

from cart.models import Order_items


from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
@method_decorator(login_required,name="dispatch")
class Addtocart(View):
    def get(self,request,i):
        #product
        p=Product.objects.get(id=i)#checks whether the product is already added to cart table
        #user
        u=request.user
        try:
            c=Cart.objects.get(user=u,product=p)
            c.quantity+=1#increments quantity by 1
            c.save()
        except:#if product does not exist
            c=Cart.objects.create(user=u,product=p,quantity=1)#creates a new record with quantity=1
            c.save()
        return redirect('cart:cartview')


class CartView(View):
    def get(self,request):
        u=request.user
        c=Cart.objects.filter(user=u)
        total=0
        for i in c:
            total=total+i.subtotal()
        context={'cart':c,'total':total}
        return render(request,'cart.html',context)

class Cartdecrement(View):
    def get(self,request,i):
        try:
            c=Cart.objects.get(id=i)
            if(c.quantity>1):
                c.quantity-=1
                c.save()
            else:
                c.delete()
        except:
            pass
        return redirect('cart:cartview')

class Cartremove(View):
    def get(self,request,i):
        try:
            c=Cart.objects.get(id=i)
            c.delete()
        except:
            pass
        return redirect('cart:cartview')
import uuid
from cart.forms import OrderForm
class Checkout(View):
    def post(self,request):
        form_instance=OrderForm(request.POST)
        if form_instance.is_valid():
            o=form_instance.save(commit=False)
            #adds current user
            u=request.user
            o.user=u


            #adds total amount
            c=Cart.objects.filter(user=u)
            total=0
            for i in c:
                total+=i.subtotal()
                print(total)
                o.amount=total
                o.save()
                if(o.payment_method=="ONLINE"):
                    #create a razorpay connetion using keys
                    client=razorpay.Client(auth=('rzp_test_RnTSdnViOdXHUR','YWDjwbgKbd7PiKeaiQ7WyiT7'))
                    #2 creates a new order in razorpsy
                    response_payment=client.order.create({'amount':(o.amount)*100,'currency':'INR'})
                    print(response_payment)
                    #retrieves the order id from the response_payment
                    id=response_payment['id']
                    #saves it in order table
                    o.order_id=id
                    o.save()
                    context={'payment':response_payment}
                    return render(request,'payment.html',context)

                else:  # COD
                    # updates order table
                    id = 'ord_cod' + uuid.uuid4().hex[:14]
                    o.order_id = id
                    o.is_ordered = True
                    o.save()
                    # add products to order_items
                    for i in c:
                        item = Order_items.objects.create(order=o, product=i.product, quantity=i.quantity)
                        item.save()
                        item.product.stock -= i.quantity
                        item.product.save()
                        # delete cart table
                    c.delete()
                    return render(request, 'payment.html')
                    pass

    def get(self,request):
        form_instance=OrderForm()
        context={'form':form_instance}
        return render(request,'checkout.html',context)

# @csrf_exempt
# def f():
#     pass

#csrf_exempt-to ignore csrf verification
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from cart.models import Order,Order_items
@method_decorator(csrf_exempt,name="dispatch")
class Payment_success(View):
    def post(self,request):
        print(request.user.username)
        response=request.POST
        # print(response)
        #updates order table
        id=response['razorpay_order_id']#READS THE ORDER ID FROM THE RAZORPAY RESPONSE
        o=Order.objects.get(order_id=id)#RETRIEVES THE ORDER RECORD MATCHING WITH THID ORDERID
        o.is_ordered=True#set is_ordered status to true
        o.save()
        #add products into order_items table
        u=request.user
        c=Cart.objects.filter(user=u)
        for i in c:
            item=Order_items.objects.create(order=o,product=i.product,quantity=i.quantity)
            item.save()
            item.product.stock-=i.quantity
            item.product.save()
        #delete cart table
        c.delete()
        return render(request,'payment_success.html')

class Yourorder(View):
    def get(self, request):
        user = request.user
        orders = Order.objects.filter(user=user).order_by('-id')
        context = {'orders': orders}
        return render(request, 'yourorder.html', context)