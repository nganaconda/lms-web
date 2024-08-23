from django import forms
from .models import Users, Question, Attribute
from django.forms import ModelForm

class UserModelForm(ModelForm):
    class Meta:
        model = Users
        fields = "__all__"

class AttributeForm(forms.ModelForm):
    class Meta:
        model = Attribute
        fields = ['answer']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question', 'type', 'difficulty', 'rightAnswer', 'professor']

    attributes = forms.ModelMultipleChoiceField(
        queryset=Attribute.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )