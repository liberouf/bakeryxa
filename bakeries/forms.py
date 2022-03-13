from django import forms
from django.contrib.auth.models import User
from .models import ghanadi,mahsool,ReviewRating





class mahsoolForm(forms.ModelForm):
   
    class Meta: 
        model = mahsool
        fields = [ 'name', 'images', 'description', 'stock', 'price' ]


    def __init__(self, *args, **kwargs):
        super(mahsoolForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = ' esmesh chie hala '
        self.fields['price'].widget.attrs['placeholder'] = ' chand hast hala '
        self.fields['description'].widget.attrs['placeholder'] = ' dg chi? harfi sokhani '
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject', 'review', 'rating']
