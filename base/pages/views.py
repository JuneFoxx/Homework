from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, JsonResponse, HttpRequest
from .form import UserForm, ImageForm
from .models import Image
from django.db import IntegrityError

def contacts(request):
    return render(request, 'pages/contacts.html')

def gallery(request):
    images = Image.objects.filter(pk__in=range(1, 5))
    return render (request, 'pages/gallery.html', context={"images": images})

def index(request):
    heroname = "мир котиков"
    descriptions = "присоединяйтесь к сообществу любителей кошек со всего мира. \
    Делимся советами, историями и бесконечной любовью к нашим пушистым друзьям."

    images = Image.objects.filter(pk__in=range(1, 5)) #__gt, lt, constraints. get/all/filter/exclude
    
    return render(request, 'pages/index.html', context={ 
        'heroname': heroname,
        'descriptions': descriptions,
        'images': images
    })

def contacts(request: HttpRequest):
    if request.method == "POST":
        form = request.POST.get('url')
        try:
            # image = Image.objects.filter(id=6).delete()
            image = Image.objects.filter(id=6).update(url=form)
            return JsonResponse({'success':image.url})
        except IntegrityError:
            return JsonResponse({'success':False})
            
    elif request.method == "GET":   
        userform = ImageForm()
        return render(request, 'pages/contacts.html', context={'form': userform})

def about(request):
    return render(request, 'pages/about.html')

def page(request, page: str):
    return HttpResponse(f"hello! {page}")

def products(request, id: int) -> HttpResponse:
    
    try:
       some = request.GET.get('some', )
    except Exception:
        return HttpResponseBadRequest()
    
    return HttpResponse(f"hello! {id}, some: {some}")

def first_page(request):
    return HttpResponseRedirect('/page')

def json_get(request):
    return JsonResponse({'name': "Kolya", "list": ["123", 1231, "some"]})