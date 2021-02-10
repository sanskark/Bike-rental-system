from django.shortcuts import render
from .models import Location
def home(request):
    location_data = Location.objects.all()
    return render(request, 'bikerental/home.html', {'location_data': location_data})