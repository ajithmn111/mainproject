from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from shop.models import Category,Product
from django.shortcuts import render, redirect
# Create your views here.
class CategoryView(View):
    def get(self,request):
        c=Category.objects.all()
        context={'cat':c}
        return render(request,'categories.html',context)
class ProductView(View):
    def get(self,request,i):
        c=Category.objects.get(id=i)
        context={'cat':c}
        return render(request,'products.html',context)

class ProductDetailView(View):
    def get(self,request,i):
        p=Product.objects.get(id=i)
        context={'product':p}
        return render(request,'productdetail.html',context)

from shop.forms import SignupForm
class Register(View):
    def post(self, request):
        form_instance = SignupForm(request.POST, request.FILES)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:userlogin')

        # return form with errors if invalid
        context = {'form': form_instance}
        return render(request, 'register.html', context)

    def get(self, request):
        form_instance = SignupForm()
        context = {'form': form_instance}
        return render(request, 'register.html', context)

from django.utils.decorators import method_decorator
from shop.forms import CategoryForm,ProductForm
from django.contrib.auth.decorators import login_required

def admin_required(fun):
    def wrapper(request):
        if not request.user.is_superuser:
            return HttpResponse("not allows")

        else:
            return fun(request)
    return wrapper
@method_decorator(admin_required,name="dispatch")
@method_decorator(login_required,name="dispatch")
class AddCategory(View):
    def post(self, request):
        form_instance = CategoryForm(request.POST, request.FILES)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:categories')

        # If form is not valid, re-render the form page
        context = {'form': form_instance}
        return render(request, 'addcategory.html', context)

    def get(self, request):
        form_instance = CategoryForm()
        context = {'form': form_instance}
        return render(request, 'addcategory.html', context)

@method_decorator(login_required,name="dispatch")
class AddProduct(View):
    def post(self, request):
        form_instance = ProductForm(request.POST,request.FILES)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:categories')

    def get(self, request):
        form_instance = ProductForm()
        context = {'form': form_instance}
        return render(request, 'addproduct.html', context)


from shop.forms import Loginform
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
class Userlogin(View):
    def get(self,request):
        form_instance=Loginform()
        context={'form':form_instance}
        return render(request,'login.html',context)

    def post(self,request):
        form_instance=Loginform(request.POST)
        if form_instance.is_valid():
            data=form_instance.cleaned_data
            u=data['username']
            p=data['password']
            user=authenticate(username=u,password=p)
            if user:
                login(request,user)
                return redirect('shop:categories')
            else:
                messages.error(request,"invalid user credentials")
                return redirect('shop:userlogin')


class Userlogout(View):
    def get(self,request):
        logout(request)
        return redirect('shop:userlogin')

class Addstockview(View):
    def post(self,request,i):
        p=Product.objects.get(id=i)
        form_instance=Stockform(request.POST,instance=p)

        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:categories')
        else:
            print('error')
            return render(request,"addstock.html",{'form':form_instance})
    def get(self,request,i):
        p=Product.objects.get(id=i)
        form_instance=stockform(instance=p)
        context={'form':form_instance}
        return render(request,'addstock.html',context)
