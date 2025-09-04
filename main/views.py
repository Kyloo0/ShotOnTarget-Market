from django.shortcuts import render

# Create your views here.
def show_main_page(request):
    context = {
        'name' : 'Fitto Fadhelli Voltanie Ariyana',
        'npm' : '2406423401',
        'class' : 'PBP F'
    }

    return render(request, 'main.html', context)

def not_found_error_page(request, exception):
    return render(request, 'notfound.html', status=404)
