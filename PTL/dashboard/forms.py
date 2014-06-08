from django import forms
from dashboard.models import Community, SysterUser
from django.contrib.auth.models import User


class CommunityForm(forms.ModelForm):

    """name = forms.CharField(max_length=255, help_text="Please enter the Community name.")
    email = forms.EmailField(max_length=255 )
    mailing_list = forms.EmailField(max_length=255)
    resource_area = forms.URLField(max_length=255)
    admin = forms.CharField(max_length=255)
    website = forms.URLField(max_length=255)
    facebook = forms.URLField(max_length=255)
    googleplus = forms.URLField(max_length=255)
    twitter = forms.URLField(max_length=255)"""

    class Meta:
        model = Community
        exclude = ('members',)


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    repeat_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class SysterUserForm(forms.ModelForm):

    class Meta:
        model = SysterUser
        fields = ('country', 'BlogURL', 'HomepageURL', 'Profilepicture')


class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name')
