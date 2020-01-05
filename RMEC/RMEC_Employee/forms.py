from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,Group
from django.contrib.auth import get_user_model,password_validation
User = get_user_model()
from django.forms import widgets
from .models import RMEC_Employee  
from django.contrib.auth.forms import PasswordResetForm,PasswordChangeForm
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from django.template import loader
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django.utils.translation import gettext, gettext_lazy as _

class SignUpForm(UserCreationForm):

    first_name = forms.CharField(max_length=30, required=False,)
    last_name = forms.CharField(max_length=30, required=False,)
    email = forms.EmailField(max_length=254,)
    phone=forms.IntegerField(required=False,)
    business_name=forms.CharField(max_length=200, required=False,)
    business_address=forms.CharField(max_length=200, required=False,)
    city=forms.CharField(max_length=200, required=False,)
    state=forms.CharField(max_length=200, required=False,)
    zip_code=forms.IntegerField(required=False,)
    

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone','email', 'business_name','business_address','city','state','zip_code')
    def clean_email(self):
        # Get the email
        email = self.cleaned_data.get('email')
        # Check to see if any users already exist with this email as a username.
        try:
            match = User.objects.get(email=email)
            print("-------in try------")
        except User.DoesNotExist:
            # Unable to find a user, this is fine
            print("-------in except------")
            return email

        # A user was found with this as a username, raise an error.
        raise forms.ValidationError('This email address is already in use.')


class AdminSignUpForm(UserCreationForm):
    
    first_name = forms.CharField(max_length=30, required=False,)
    last_name = forms.CharField(max_length=30, required=False,)
    email = forms.EmailField(max_length=254,)

    

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email','is_superuser','is_active','is_staff')
class DateInput(forms.DateInput):
    input_type = 'date'
class Mymultiselect(forms.SelectMultiple):
    pass
class ParticipantForm(forms.ModelForm):  
    class Meta:  
        model = RMEC_Employee  
        fields = "__all__"  
        widgets = {
            'hired_date': DateInput(),
            'created_date': DateInput(),
            'updated_date':DateInput(),
            'certificate':Mymultiselect(),
            'work_area':Mymultiselect()
        }
    def __init__(self, *args, **kwargs):
        super(ParticipantForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
class CustomPasswordResetForm(PasswordResetForm):
    pass
# class UsersUpdateForm(forms.ModelForm):
#     class Meta:
#         model=User
#         fields = ('username','email','first_name','last_name','is_active')
class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autofocus': True,'placeholder':'Old password',"class":"password-input"}),
    )
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'autofocus': True,'placeholder':'New password',"class":"password-input"}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autofocus': True,'placeholder':'New password Confirmation',"class":"password-input"}),
    )

        

    