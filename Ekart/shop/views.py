from django.shortcuts import render
from shop.models import Product,OrderUpdate,Order,User
# Create your views here.
def index(request):

    allProds = []
    cats = Product.objects.values('category')
    set1 = {item['category'] for item in cats}
    print(cats)
    for cat in set1:
        prod = Product.objects.filter(category = cat)
        allProds.append([prod,cat])
    param = {'allProds' : allProds}
    return render(request,"shop/index.html",param)

def about(request):
    return render(request,"shop/about.html")

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        phone = request.POST.get('phone','')
        query = request.POST.get('text','')
        user= User(name = name,email = email,phone = phone,query = query)
        user.save()
    return render(request,"shop/Contactus.html")

def tracker(request):
    if(request.method == 'POST'):

        email = request.POST.get('inputemail','')
        orderid = request.POST.get('inputid','')
        try:

            order = Order.objects.filter(order_id=orderid,email = email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id = orderid)
                updates =[]
                for item in update:
                    updates.append({'text':item.update_desc,'time' : item.timestamp})
                    response = json.dumps([updates,order[0].order_items],default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}{}')
    return render(request, 'shop/tracker.html')



def products(request,myid):
    product = Product.objects.filter(id = myid)
    return render(request,"shop/products.html",{'product':product[0]})

def queryMatch(query,item):
    if query.lower() in item.desc.lower() or query.lower() in item.product_name.lower() or query.lower() in item.category.lower():
        return True
    return False
def search(request):
    query = request.POST.get('search')
    print("this is my query" +query)
    allProds = []
    cats = Product.objects.values('category')
    set1 = {item['category'] for item in cats}
    for cat in set1:
        prod = Product.objects.filter(category = cat)
        selected_list = [item for item in prod if queryMatch(query,item)]
        print(selected_list)
        allProds.extend(selected_list)
    param = {'allProds' : allProds}
    print(allProds)
    return render(request,"shop/search.html",param)

def checkout(request):
    thank = 0
    if request.method == "POST":
        item_json = request.POST.get('json','')
        print("muskan")
        print(item_json)
        print("muskan1")
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        address = request.POST.get('address1','') +" "+ request.POST.get('address2','')
        city = request.POST.get('city','')
        state = request.POST.get('state','')
        zip_code = request.POST.get('zip','')
        phone = request.POST.get('phone','')
        order = Order(order_items=item_json,name = name,email = email,phone = phone,address=address,city=city,state=state,zip_code=zip_code)
        order.save()
        update = OrderUpdate(order_id = order.order_id,update_desc="the order has been placed")
        update.save()
        thank = 1
    return render(request,"shop/checkout.html",{'thank':thank})
