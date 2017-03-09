from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
# from main.models import Teacher, Student

# map internal, external choice values
USER_GROUP_CHOICES = (
    ('students','student'),
    ('teachers', 'teacher')
    )

# ideally create logic that presets radio button as checked depending on
# referring url, i.e. /students/ or /teachers/
class LoginForm(forms.Form):
    login_type = forms.ChoiceField(label='I am a:', widget=forms.RadioSelect, \
        choices=USER_GROUP_CHOICES)
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        login_type = self.cleaned_data['login_type']

        user_qs = User.objects.filter(username=username)
        if user_qs.count() == 0:
            raise forms.ValidationError("Invalid username")
        if user_qs.count() == 1:
            user = user_qs.first()
        if username and password:
            auth_user = authenticate(username=username, password=password)
            if login_type != auth_user.profile.get_role():
                raise forms.ValidationError("Incorrect user type")
            if not auth_user:
                raise forms.ValidationError("Incorrect password")
            if not auth_user.is_active:
                raise forms.ValidationError("User is not active")
        else:
            raise forms.ValidationError("Username and password fields are required")
        return super(LoginForm, self).clean(*args, **kwargs)
