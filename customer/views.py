from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render,HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.views.generic import CreateView
from bikerental.models import User
from bike.models import Booking
from .forms import CustomerSignupForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomerUpdateForm, CustomerProfileUpdateForm
from datetime import date

# Create your views here.

class customer_signup(CreateView):
    model = User
    form_class = CustomerSignupForm
    template_name = 'customer/signup.html'

    def form_valid(self, form):
        user = form.save()
        # login(self.request, user)
        return redirect('customer-login')

def customer_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_customer:
                login(request, user)
                return redirect('home')
            elif user.is_dealer:
                messages.info(request, 'User does not exist')
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'customer/login.html',
                  context={'form': AuthenticationForm()})

def customer_logout(request):
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    if request.method == 'POST':
        c_form = CustomerUpdateForm(request.POST, instance=request.user)

        cp_form = CustomerProfileUpdateForm(request.POST,
                                            request.FILES,
                                            instance=request.user.profile)

        if c_form.is_valid():
            c_form.save()
            messages.success(request,
                             f'Your account has been updated!')
            return redirect('customer-profile')

        if cp_form.is_valid():
            cp_form.save()
            messages.success(request,
                             f'Your account has been updated!')
            return redirect('customer-profile')
    else:
        c_form = CustomerUpdateForm(instance=request.user)
        cp_form = CustomerProfileUpdateForm(instance=request.user.profile)

    context = {
        'c_form': c_form,
        'cp_form': cp_form
    }
    return render(request, 'customer/profile.html', context)

@login_required
def my_rides(request):
    all_booking = list(Booking.objects.all())
    loggedin_userid = request.user.id
    user_booking = []
    count = 0

    for b in all_booking:
        if str(b.customer.user_id) == str(loggedin_userid):
            if date.today() > b.dropoff_date:
                b.is_completed = True
                b.save()
            user_booking.append(b)
            count = count + 1
    # return HttpResponse(count)
    return render(request,'customer/myrides.html',{'user_booking': user_booking})

def cancel_booking(request):
    if request.method == "POST":
        booking_id=request.POST['cancelbutton']
        current_booking = Booking.objects.get(booking_id=booking_id)

        if date.today() < current_booking.pickup_date:
            Booking.objects.get(booking_id=booking_id).delete()
            messages.success(request, 'Your ride has been canceled successfully!')
            return redirect('customer-myrides')
        messages.warning(request, 'You can not cancel this ride!')
        return redirect('customer-myrides')

    return redirect('customer-myrides')