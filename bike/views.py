from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from bike.models import Bike
# Create your views here.

@login_required
def bikes_list(request):
    if request.method == 'POST':
        all_bikes = list(Bike.objects.all())
        selected_city = request.POST['selectedcity']
        selected_bikes = []

        count = 0
        for b in all_bikes:
            if str(b.bike_location).lower() == str(selected_city).lower() and b.is_confirmed and not b.is_on_halt:
                selected_bikes.append(b)
                count = count + 1

        if count != 0:
            return render(request, 'bike/viewbike.html', {'selected_bikes': selected_bikes})

        return HttpResponse('<h1 class="display-1">No bike available in selected city</h1>')

    return redirect('/')