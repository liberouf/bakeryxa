from django import forms
from .models import Account 
from bakeries.models import ghanadi
from django.utils.text import slugify
from django.contrib.gis import forms
from leaflet.forms.widgets import LeafletWidget



 
class accountsForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
        'class': 'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password'
    }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'position', 'email', 'password']
        widgets = {'position': LeafletWidget(  attrs={
                         'map_width': 800,
                         'map_height': 400,
                         'default_lat': 35.715298,
                         'default_lon': 51.404343,
                         'default_zoom': 9
                        })}

      

    def clean(self):
        cleaned_data = super(accountsForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match!"
            )

    def __init__(self, *args, **kwargs):
        super(accountsForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter last Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


######################################################################################################    Owner


##########################################################################################    ghanadi

class ghanadiForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
        'class': 'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password'
    }))

    class Meta: 
        model = ghanadi
        fields = [ 'name', 'phone', 'address',  'position', 'images', 'password']
        location_name = forms.CharField(label='Name', max_length=20)
        widgets = {'position': LeafletWidget(  attrs={
                         'map_width': 800,
                         'map_height': 400,
                         'default_lat': 35.715298,
                         'default_lon': 51.404343,
                         'default_zoom': 9
                        })}

    def clean(self):
        cleaned_data = super(ghanadiForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match!"
            ) 

    def __init__(self, *args, **kwargs):
        super(ghanadiForm, self).__init__(*args, **kwargs)
        #self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        #self.fields['last_name'].widget.attrs['placeholder'] = 'Enter last Name'
        
        self.fields['phone'].widget.attrs['placeholder'] = 'Enter Phone Number'
        #self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'



