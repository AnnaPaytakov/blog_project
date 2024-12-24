from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django import forms
from .models import Profile
from django.forms import ModelForm
from django.forms.widgets import ClearableFileInput
from django.utils.translation import gettext_lazy as _

class CustomClearableFileInput(ClearableFileInput):
    initial_text = _('Current photo')
    input_text = _('Edit')
    clear_checkbox_label = _('Clear')

class AccountForm(ModelForm):
    class Meta:
        model = Profile
        fields = [
            'username', 'firstname', 'lastname', 'profile_image', 'email',
        ]
        widgets = {
            'profile_image': CustomClearableFileInput(attrs={'class': 'form-control-file'}),
            'start_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'finish_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Enter username'
        self.fields['email'].widget.attrs['placeholder'] = 'example@gmail.com'
        self.fields['firstname'].widget.attrs['placeholder'] = 'Enter your name'
        self.fields['lastname'].widget.attrs['placeholder'] = 'Enter your surname'
        self.fields['profile_image'].widget.attrs.update({'class':'form-control-file'})
        

class CustomRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    
    def __init__(self, *args, **kwargs):
        super(CustomRegisterForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Confirm Password'

        self.fields['username'].widget.attrs['placeholder'] = 'Enter username'
        self.fields['email'].widget.attrs['placeholder'] = 'example@gmail.com'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter your name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter your surname'
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm password'