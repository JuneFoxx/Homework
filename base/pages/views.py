from django.shortcuts import render
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, JsonResponse, HttpRequest
from dataclasses import dataclass
from .form import ImageModelForm, ImageForm
from .models import Image
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView

@dataclass
class Person:
    name: str
    age: str



# def index(request):
#     heroname = "мир котиков"
#     descriptions = "присоединяйтесь к сообществу любителей кошек со всего мира. \
#     Делимся советами, историями и бесконечной любовью к нашим пушистым друзьям."
#     images = Image.objects.exclude(pk__in = [7]) #__gt, lt, lte, gte, constrains. get/all/filter/exclude
#     return render(request, 'pages/index.html', context={ 
#         'heroname': heroname,
#         'descriptions': descriptions,
#         'images': images
        
#     })

class IndexView(TemplateView):
    template_name = 'pages/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heroname'] = "мир котиков"
        context['descriptions'] = "присоединяйтесь к сообществу любителей кошек со всего мира. \
    Делимся советами, историями и бесконечной любовью к нашим пушистым друзьям."
        context['images'] = Image.objects.exclude(pk__in = [7])
        return context




def contacts(request: HttpRequest):
    if request.method == "POST":
        form = request.POST.get('url')
        try: 
            # image = Image.objects.filter(id=6).update(url=form)
            image = Image.objects.filter(id=7).delete()
            return JsonResponse({'sucesee': image})
        except IntegrityError:
            return JsonResponse({'sucesee': False})
    elif request.method == 'GET':
        userform = ImageForm()
        return render(request, 'pages/contacts.html', context={'form': userform})


class ContactsCreateView(CreateView):
    model = Image
    # form_class = ImageForm
    fields = ['url', "slug"]
    template_name = 'pages/contacts.html'
    success_url = "/"


class ContactsUpdateView(UpdateView):
    model = Image
    form_class = ImageModelForm
    template_name = 'pages/contacts.html'
    success_url = "/"

class ContactsDeleteView(UpdateView):
    model = Image
    template_name = 'pages/confirm_delete.html'
    success_url = "/"

    
# # Дополнительный 
# def about(request):
#     return render(request, 'pages/about.html')
# Image.objects.all()



# Основной инструмент
class AboutView(TemplateView):
    template_name = 'pages/about.html'



def page(request, page: str):
    return HttpResponse(f"hello! {page}")

class GalleryView(ListView):
    model = Image
    template_name ='pages/gallery.html'
    context_object_name = "images"
    ordering = ['-id']
    
    def get_queryset(self):
        return Image.objects.filter(id__gt=3)
    

class GalleryDetailView(DetailView):
    model = Image
    template_name = "pages/image.html"
    context_object_name = "image"
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


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
