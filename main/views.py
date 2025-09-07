from django.shortcuts import render

# Create your views here.
def show_main(request):
    context = {
        'project' : 'majulah shop',
        'name': 'Khawarizmi Aydin',
        'class': 'PBP D'
    }

    return render(request, "main.html", context)