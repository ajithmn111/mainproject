from django.shortcuts import render
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
        form_instance = SignupForm(request.POST,request.FILES)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:userlogin')


    def get(self, request):
        form_instance=SignupForm()
        context = {'form': form_instance}
        return render(request, 'register.html', context)

from shop.forms import CategoryForm,ProductForm
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
