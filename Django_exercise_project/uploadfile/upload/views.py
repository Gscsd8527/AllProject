from django.shortcuts import render, HttpResponse
from upload.models import Product
# Create your views here.
def Upload(request):
    return HttpResponse('Hello World')

def show(request):
    products = Product.objects.all()[1]
    title = products.title
    img = products.image.url
    print('---------------------')
    print(img)
    print(type(img))
    print('---------------------')
    context = {
        'title': title,
        'img': img
    }
    return render(request, 'uplode/show.html', context)
