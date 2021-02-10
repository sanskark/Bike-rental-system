from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Dealer, DealerProfile
from django.db import transaction
from bikerental.models import User

class DealerRegisterForm(UserCreationForm):
    email = forms.EmailField()
    mobile_no = forms.DecimalField(max_digits=10, decimal_places=0)
    password1 = forms.CharField(label='Enter Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields=['username', 'email', 'mobile_no', 'password1', 'password2']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_dealer = True
        user.save()

        dealer = Dealer.objects.create(user=user)
        dealer.email = self.cleaned_data.get('email')
        dealer.mobile_no = self.cleaned_data.get('mobile_no')
        dealer.save()
        return user

class DealerUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username',
                  'email']

class DealerExtraInfoUpdateForm(forms.ModelForm):
    class Meta:
        model = Dealer
        fields = ['mobile_no']
        help_texts = {
            'mobile_no': 'Press Enter',
        }

# customer profile update form
class DealerProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = DealerProfile
        fields = ['profile_pic']

        labels ={
            'profile_pic':'Profile Picture'
        }

        help_texts={
            'profile_pic':'Change profile picture here',
        }

        widgets={
            'profile_pic':forms.FileInput(attrs={'class':'form-control-file'})
        }