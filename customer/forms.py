from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import  Customer, Profile
from django.db import transaction
from bikerental.models import User

class CustomerSignupForm(UserCreationForm):
    email = forms.EmailField()
    password1 = forms.CharField(label='Enter Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields=['username', 'email', 'password1', 'password2']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.save()

        customer = Customer.objects.create(user=user)
        customer.email = self.cleaned_data.get('email')
        customer.save()
        return user

# customer update form
class CustomerUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username',
                  'email']

# customer profile update form
class CustomerProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['mobile_no',
                  'profile_pic',
                  'id_proof',
                  'driving_license']

        labels ={
            'mobile_no' : 'Mobile Number',
            'profile_pic':'Profile Picture',
            'id_proof': 'ID proof',
            'driving_license': 'Driving license'
        }

        help_texts={
            'profile_pic':'Change profile picture here',
            'id_proof': 'Add your ID here',
            'driving_license': 'Add your driving license here'
        }

        widgets={
            'profile_pic':forms.FileInput(attrs={'class':'form-control-file'}),
            'id_proof': forms.FileInput(attrs={'class':'form-control-file'}),
            'driving_license': forms.FileInput(attrs={'class':'form-control-file'})
        }