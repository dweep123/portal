from django import forms
from dashboard.models import SysterUser, Community, News, CommunityPage
from django.contrib.auth.models import User


class CommunityForm(forms.ModelForm):

    class Meta:
        model = Community


class NewsEditForm(forms.ModelForm):

    class Meta:
        model = News
        exclude = ('community',)

class NewsAddForm(forms.ModelForm):

    class Meta:
        model = News
        exclude = ('community','author')

class PageAddForm(forms.ModelForm):

    class Meta:
        model = CommunityPage
	fields = ['title','slug','editor']
