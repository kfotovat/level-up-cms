from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from .forms import LoginForm
from main.models import School, Profile
# from main.views import get_credentials

def login_view(request, login_type=None, school_slug=None):
    if request.method == 'POST':
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            login_type = form.cleaned_data['login_type']
            user = authenticate(username=username, password=password)
            login(request, user)
            context = user.profile.add_credentials_to_context({})
            # print "login view:", context
            return redirect('welcome', username=context['username'], login_type=context['login_type'], school_slug=context['school_slug'])
            # return redirect('welcome', context)

    if request.method == 'GET' and login_type is not None:
        title = "this is the login form for {}!".format(login_type)
        form = LoginForm(initial={'login_type': login_type})
        # add in redirect logic
    else:
        title = "this is the generic login form!"
        form = LoginForm()
    return render(request, "login.html", {'title': title, 'form': form})


def logout_view(request):
    leaving_user = request.user
    logout(request)
    # add in redirect logic
    return render(request, "logout.html", { "leaving_user": leaving_user })
