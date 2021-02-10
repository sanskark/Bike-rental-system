from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.views.generic import CreateView
from .forms import DealerRegisterForm, DealerUpdateForm, DealerProfileUpdateForm, DealerExtraInfoUpdateForm
from bikerental.models import User, Location
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from bike.models import Bike

# Create your views here.

class dealer_register(CreateView):
    model = User
    form_class = DealerRegisterForm
    template_name = 'dealer/signup.html'

    def form_valid(self, form):
        user = form.save()
        # login(self.request, user)
        return redirect('dealer-login')

def dealer_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_dealer:
                login(request, user)
                return redirect('home')
            elif user.is_customer:
                messages.info(request, 'User does not exist')
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'dealer/login.html',
                  context={'form': AuthenticationForm()})

def dealer_logout(request):
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    if request.method == 'POST':
        d_form = DealerUpdateForm(request.POST, instance=request.user)
        dinfo_form = DealerExtraInfoUpdateForm(request.POST, instance=request.user.dealer)
        dp_form = DealerProfileUpdateForm(request.POST, request.FILES,
                                            instance=request.user.dealerprofile)


        if d_form.is_valid():
            d_form.save()
            messages.success(request,
                             f'Your account has been updated!')
            return redirect('dealer-profile')

        if dinfo_form.is_valid():
            dinfo_form.save()
            messages.success(request,
                             f'Your account has been updated!')
            return redirect('dealer-profile')

        if dp_form.is_valid():
            dp_form.save()
            messages.success(request,
                             f'Your account has been updated!')
            return redirect('dealer-profile')


    else:
        d_form = DealerUpdateForm(instance=request.user)

        dp_form = DealerProfileUpdateForm(instance=request.user.dealerprofile)
        dinfo_form = DealerExtraInfoUpdateForm(instance=request.user.dealer)

    context = {
        'd_form': d_form,
        'dp_form': dp_form,
        'dinfo_form': dinfo_form,
    }
    return render(request, 'dealer/profile.html', context)

def add_bike(request):
    locations = list(Location.objects.all())

    return render(request, 'dealer/addbike.html',{'locations': locations})

@login_required
def add_new_bike(request):
    if request.method == 'POST' and request.user.is_authenticated:
        com_name = request.POST['company_name']
        mod_name = request.POST['model_name']
        regs_number = request.POST['reg_number']
        seat_cap = request.POST['seat_capcity']
        curr_location = request.POST['cur_location']
        rpd  = request.POST['rent_per_day']
        drivenkms = request.POST['driven_kms']
        pickup_add = request.POST['pickup_add']
        dropoff_add = request.POST['dropoff_add']
        bikeimg = request.FILES.get('bike_image')

        # logic to remove duplication of bikes
        all_bikes = Bike.objects.all()
        for bike in all_bikes:
            if bike.reg_number.lower() == regs_number.lower():
                messages.warning(request, 'Bike with this registration number already registered')
                return redirect('dealer-addbike')

        new_bike = Bike()
        new_bike.owner = request.user.dealer
        new_bike.bike_company = com_name
        new_bike.bike_model = mod_name
        new_bike.reg_number = regs_number
        new_bike.seat_capacity = seat_cap
        new_bike.bike_location = Location.objects.get(location_name = curr_location)
        new_bike.rent_per_day = rpd
        new_bike.driven_kms = drivenkms
        new_bike.pickup_add = pickup_add
        new_bike.dropoff_add = dropoff_add
        new_bike.image = bikeimg

        new_bike.save()
        return redirect('dealer-mybikes')
    return redirect('home')

@login_required
def my_bikes(request):
    all_bikes = list(Bike.objects.all())
    loggedin_userid = request.user.id
    user_bikes = []
    count = 0

    for b in all_bikes:
        if str(b.owner_id)== str(loggedin_userid):
            user_bikes.append(b)
            count=count+1

    if count != 0:
        return render(request, 'dealer/mybikes.html',{'user_bikes':user_bikes})
    return HttpResponse('<h1>No bike added</h1>')

@login_required
def delete_bike(request):
    if request.method == "POST":

        id = request.POST['deletebutton']
        Bike.objects.get(bike_id = id).delete()
        return redirect('dealer-mybikes')
    return redirect('/')

@login_required
def edit_bike(request):
    if request.method == "POST":
        id = request.POST['editbutton']
        bike = Bike.objects.get(bike_id=id)

        locations = list(Location.objects.all())

        return render(request, 'dealer/editbike.html',{'bike': bike, 'locations':locations})
    return redirect('/')

@login_required
def apply_bike(request):
    if request.method == "POST":
        id = request.POST['applybutton']
        bike = Bike.objects.get(bike_id=id)

        com_name = request.POST['company_name']
        mod_name = request.POST['model_name']
        regs_number = request.POST['reg_number']
        seat_cap = request.POST['seat_capcity']
        curr_location = request.POST['cur_location']
        rpd = request.POST['rent_per_day']
        drivenkms = request.POST['driven_kms']
        pickup_add = request.POST['pickup_add']
        dropoff_add = request.POST['dropoff_add']
        bikeimg = request.FILES.get('bike_image')

        all_bikes = list(Bike.objects.all())


        for b in all_bikes:
            if b.bike_id != int(id):
                if b.reg_number.lower() == regs_number.lower():
                    messages.warning(request, 'Bike with this registration number already registered')
                    return redirect('dealer-mybikes')

        bike.bike_company = com_name
        bike.bike_model = mod_name
        bike.reg_number = regs_number
        bike.seat_capacity = seat_cap
        bike.bike_location = Location.objects.get(location_name=curr_location)
        bike.rent_per_day = rpd
        bike.driven_kms = drivenkms
        bike.pickup_add = pickup_add
        bike.dropoff_add = dropoff_add

        if bikeimg is not None:
            bike.image = bikeimg

        bike.save()

        return redirect('dealer-mybikes')
    return redirect('dealer-mybikes')

@login_required
def hold_bike(request):
    if request.method == "POST":
        # id_put = request.POST['put_on_hold']
        # id_remove = request.POST['remove_hold']
        # bike = Bike.objects.get(bike_id = id)
        # if id_put is None:
        #     bike = Bike.objects.get(bike_id = id_remove)
        #     bike.is_on_halt = False
        # if id_remove is None:
        #     bike = Bike.objects.get(bike_id=id_put)
        #     bike.is_on_halt = True

        if 'put_on_hold' in request.POST:
            id = request.POST['put_on_hold']
            bike = Bike.objects.get(bike_id=id)
            bike.is_on_halt=True
            bike.save()

        if 'remove_hold' in request.POST:
            id = request.POST['remove_hold']
            bike = Bike.objects.get(bike_id=id)
            bike.is_on_halt=False
            bike.save()

        return redirect('dealer-mybikes')
    return redirect('dealer-mybikes')
