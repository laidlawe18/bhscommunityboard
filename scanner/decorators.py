from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import logout

def not_login_required(view):
    """
    Only lets a user through if they're not logged in. Otherwise, redirects
    to the home page.
    """
    def new_view(request, *args, **kwargs):
        if request.user.is_authenticated():
            logout(request)
            return view(request, *args, **kwargs)
        else:
            return view(request, *args, **kwargs)
    return new_view