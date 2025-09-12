from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from main.models import Product
from main.forms import ProductForm

app_name = 'main'

# Create your views here.
def show_main_page(request):
    product_list = Product.objects.all()
    context = {
        'name' : 'Fitto Fadhelli Voltanie Ariyana',
        'npm' : '2406423401',
        'class' : 'PBP F',
        'product_list': product_list
    }

    return render(request, 'main.html', context)

def not_found_error_page(request, exception):
    return render(request, 'notfound.html', status=404)

def create_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main_page')

    context = {'form': form}
    return render(request, "product_form.html", context)

def show_xml(request):
    product_list = Product.objects.all()
    xml_data = serializers.serialize('xml', product_list)
    return HttpResponse(xml_data, content_type='application/xml')

def show_json(request):
    product_list = Product.objects.all()
    json_data = serializers.serialize('json', product_list)
    return HttpResponse(json_data, content_type='application/json')

def show_xml_by_id(request, id):
    try:
        product = Product.objects.filter(pk=id)
        xml_data = serializers.serialize('xml', product)
        return HttpResponse(xml_data, content_type='application/xml')
    except Product.DoesNotExist:
        return HttpResponse(status=404)

def show_json_by_id(request, id):
    try:
        product = Product.objects.filter(pk=id)
        json_data = serializers.serialize('json', [product])
        return HttpResponse(json_data, content_type='application/json')
    except Product.DoesNotExist:
        return HttpResponse(status=404)


