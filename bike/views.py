from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from bike.models import Bike, Booking
from bikerental.models import User
from customer.models import Customer
from django.contrib import messages
import easy_date
from datetime import date
from django.conf import settings
from django.core.mail import send_mail
import razorpay
# Create your views here.

@login_required
def bikes_list(request):
    if request.method == 'POST':
        all_bikes = list(Bike.objects.all())
        all_booking = list(Booking.objects.all())

        selected_city = request.POST['selectedcity']

        pickup_date = str(request.POST['pickupDate'])
        dropoff_date = str(request.POST['dropoffDate'])

        #pickup_date = str to date
        pickup = easy_date.convert_from_string(pickup_date, '%Y-%m-%d', '%d-%m-%Y', date)
        dropoff = easy_date.convert_from_string(dropoff_date, '%Y-%m-%d', '%d-%m-%Y', date)

        request.session['pickupDate'] = pickup_date
        request.session['dropoffDate'] = dropoff_date


        selected_bikes=[]

        for b in all_bikes:
            if str(b.bike_location).lower() == str(selected_city).lower() and b.is_confirmed and not b.is_on_halt:
                selected_bikes.append(b)

        temp_bikes = selected_bikes.copy()

        for bike in temp_bikes:
            for booking in all_booking:
                if str(booking.bike.bike_id) == str(bike.bike_id):
                    if pickup <= booking.dropoff_date and dropoff >= booking.pickup_date:
                        print(bike)
                        selected_bikes.remove(bike)

        if len(selected_bikes) != 0:
            return render(request, 'bike/viewbike.html', {'selected_bikes': selected_bikes, 'pickup': pickup, 'dropoff': dropoff, 'selected_city': selected_city})

        return HttpResponse('<h1 class="display-1">No bike available in selected city</h1>')
    return redirect('home')

@login_required
def booking(request):
    if request.method == "POST":
        id = request.POST['book_button']
        bike = Bike.objects.get(bike_id=id)

        loggedin_userid = request.user.id
        customer = User.objects.get(id=loggedin_userid)

        pickup_date = easy_date.convert_from_string(request.session['pickupDate'], '%Y-%m-%d', '%d-%m-%Y', date)
        dropoff_date = easy_date.convert_from_string(request.session['dropoffDate'], '%Y-%m-%d', '%d-%m-%Y', date)

        total_days = (dropoff_date-pickup_date).days + 1
        total_price = int(bike.rent_per_day) * int(total_days)
        return render(request,'bike/booking.html',{'bike': bike, 'customer': customer, 'pickup_date': pickup_date, 'dropoff_date': dropoff_date, 'total_days': total_days, 'total_price': total_price});
    return redirect('home')

def confirm_booking(request):
    if request.method == "POST":
        id = request.POST['confirm_book_button']
        bike = Bike.objects.get(bike_id=id)

        loggedin_userid = request.user.id
        customer = Customer.objects.get(user_id=loggedin_userid)

        if customer.user.profile.driving_license.name == 'default.jpg' and customer.user.profile.id_proof.name == 'default.jpg':
            messages.warning(request, 'Upload your ID proof and driving license before booking ride!')
            return redirect('customer-profile')

        new_booking = Booking()
        new_booking.bike = Bike.objects.get(bike_id=id)
        new_booking.customer = Customer.objects.get(user_id=loggedin_userid)
        new_booking.pickup_date= request.session['pickupDate']
        new_booking.dropoff_date= request.session['dropoffDate']

        pickup_date = easy_date.convert_from_string(request.session['pickupDate'], '%Y-%m-%d', '%d-%m-%Y',
                                                    date)
        dropoff_date = easy_date.convert_from_string(request.session['dropoffDate'], '%Y-%m-%d', '%d-%m-%Y',
                                                     date)

        total_days = (dropoff_date - pickup_date).days + 1
        total_rent = int(bike.rent_per_day) * int(total_days)

        new_booking.total_days=int(total_days)
        new_booking.total_rent=int(total_rent)

        new_booking.save()

        #to send email to customer
        username = request.user.username
        subject = 'Your booking has been confirmed'
        message = f'Dear {username}, thank you for booking a ride.\n' \
                  f'Your booking from {pickup_date} to {dropoff_date} has been confirmed\n' \
                  f'Total days: {total_days}\n' \
                  f'Total rent: {total_rent}\n' \
                  f'Please carry your original driving license and ID proof\n'
        email_from = settings.EMAIL_HOST_USER
        recipient = [request.user.email]

        send_mail(subject, message, email_from, recipient)

        messages.success(request, 'Your booking has been confirmed')
        return redirect('home')
    return redirect('home')
