from django.shortcuts import render
from django.http import HttpResponse
from blog.models import blogpost
# Create your views here.

def blogp(request,id):
    obj = blogpost.objects.filter(blogpost_id = id)
    print(obj)
    return render(request,"blog/blogpost.html",{'req_object':obj[0]})

def blog(request):
    objs = blogpost.objects.all()
    n = len(objs)

    return render(request,"blog/blog.html",{'objects':objs,'range':range(1,n+1)})
