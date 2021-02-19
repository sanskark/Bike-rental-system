from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from bike.models import Bike, Booking
from bikerental.models import User
from customer.models import Customer
from django.contrib import messages
import easy_date
import datetime
# Create your views here.

@login_required
def bikes_list(request):
    if request.method == 'POST':
        all_bikes = list(Bike.objects.all())
        selected_city = request.POST['selectedcity']

        pickup_date = str(request.POST['pickupDate'])
        dropoff_date = str(request.POST['dropoffDate'])

        request.session['pickupDate'] = pickup_date
        request.session['dropoffDate'] = dropoff_date

        selected_bikes = []

        count = 0
        for b in all_bikes:
            if str(b.bike_location).lower() == str(selected_city).lower() and b.is_confirmed and not b.is_on_halt:
                selected_bikes.append(b)
                count = count + 1

        if count != 0:
            return render(request, 'bike/viewbike.html', {'selected_bikes': selected_bikes})
            # return HttpResponse(isinstance(new_p,datetime.date))
        return HttpResponse('<h1 class="display-1">No bike available in selected city</h1>')

    return redirect('/')

@login_required
def booking(request):
    if request.method == "POST":
        id = request.POST['book_button']
        bike = Bike.objects.get(bike_id=id)

        loggedin_userid = request.user.id
        customer = User.objects.get(id=loggedin_userid)

        pickup_date = easy_date.convert_from_string(request.session['pickupDate'], '%Y-%m-%d', '%d-%m-%Y', datetime.date)
        dropoff_date = easy_date.convert_from_string(request.session['dropoffDate'], '%Y-%m-%d', '%d-%m-%Y', datetime.date)

        total_days = (dropoff_date-pickup_date).days
        total_price = int(bike.rent_per_day) * int(total_days)
        return render(request,'bike/booking.html',{'bike': bike, 'customer': customer, 'pickup_date': pickup_date, 'dropoff_date': dropoff_date, 'total_days': total_days, 'total_price': total_price});
    return redirect('home')

def confirm_booking(request):
    if request.method == "POST":
        id = request.POST['confirm_book_button']
        bike = Bike.objects.get(bike_id=id)

        loggedin_userid = request.user.id
        # customer = User.objects.get(id=loggedin_userid)

        new_booking = Booking()
        new_booking.bike = Bike.objects.get(bike_id=id)
        new_booking.customer = Customer.objects.get(user_id=loggedin_userid)
        new_booking.pickup_date= request.session['pickupDate']
        new_booking.dropoff_date= request.session['dropoffDate']

        pickup_date = easy_date.convert_from_string(request.session['pickupDate'], '%Y-%m-%d', '%d-%m-%Y',
                                                    datetime.date)
        dropoff_date = easy_date.convert_from_string(request.session['dropoffDate'], '%Y-%m-%d', '%d-%m-%Y',
                                                     datetime.date)

        total_days = (dropoff_date - pickup_date).days
        total_rent = int(bike.rent_per_day) * int(total_days)

        new_booking.total_days=int(total_days)
        new_booking.total_rent=int(total_rent)
        new_booking.save()
        messages.success(request, 'Your booking has been confirmed')
        return redirect('home')
    return redirect('home')