from django.forms import ModelForm, Textarea
from django.contrib.auth.models import User

from .models import Profile


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['email']

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['biography']
        widgets = {'biography': Textarea}
