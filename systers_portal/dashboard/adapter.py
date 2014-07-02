from allauth.account.adapter import DefaultAccountAdapter
from django.shortcuts import resolve_url


class AccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        if request.user.is_authenticated():
            url = '/dashboard/view_profile/' + request.user.username + '/'
        return resolve_url(url)

    def get_signup_redirect_url(self, request):
        if request.user.is_authenticated():
            url = '/dashboard/view_profile/' + request.user.username + '/'
        return resolve_url(url)
