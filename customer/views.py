from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.views.generic import CreateView
from bikerental.models import User
from .forms import CustomerSignupForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomerUpdateForm, CustomerProfileUpdateForm

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