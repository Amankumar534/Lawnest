from django.shortcuts import render
from .models import Attorney,News

# Create your views here.
def home(request):
    attorney = Attorney.objects.all()
    news = News.objects.all()
    return render(request, 'home.html', {'attorney': attorney, 'news': news})