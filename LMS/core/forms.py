from django import forms
from .models import Users


from django.forms import ModelForm
from .models import User

class UserModelForm(ModelForm):
    class Meta:
        model = Users
        fields = "__all__"