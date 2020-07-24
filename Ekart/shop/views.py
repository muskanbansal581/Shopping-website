from django.shortcuts import render

# Create your views here.
def index(request):

    # allProds = []
    # cats = Product.objects.values('category')
    # set1 = {item['category'] for item in cats}
    # print(cats)
    # for cat in set1:
    #     prod = Product.objects.filter(category = cat)
    #     allProds.append([prod,cat])
    # param = {'allProds' : allProds}
     return render(request,"shop/index.html")
