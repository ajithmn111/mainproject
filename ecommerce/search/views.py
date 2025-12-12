from django.shortcuts import render
from django.views import View
from shop.models import Product
from django.db.models import Q


# Create your views here.
class SearchView(View):
    def get(get, request):
        query = request.GET['q']  # reads the keyword
        print(query)
        # 0RM query to filter records from table(two or more records)
        p = Product.objects.filter(Q(name__icontains=query) |
                                Q(description__icontains=query) |
                                Q(price__icontains=query)  # case insensitive
                                )
        context = {'products': p,'query':query}
        return render(request, 'search.html', context)