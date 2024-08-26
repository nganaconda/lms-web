from django import forms
from .models import Users, Question, Attribute
from django.forms import ModelForm, modelformset_factory

class UserModelForm(ModelForm):
    class Meta:
        model = Users
        fields = "__all__"


class QuestionForm(forms.ModelForm):
    rightAnswerText = forms.CharField(label='Right Answer', max_length=100)

    class Meta:
        model = Question
        fields = ['question', 'type', 'difficulty']

    def clean_difficulty(self):
        difficulty = self.cleaned_data.get('difficulty')
        if difficulty < 1 or difficulty > 4:
            raise forms.ValidationError('Difficulty must be between 1 and 4.')
        return difficulty


# Attribute form for creating additional attributes
class AttributeForm(forms.ModelForm):
    class Meta:
        model = Attribute
        fields = ['answer']


# Formset for dynamically handling multiple attributes
AttributeFormSet = modelformset_factory(
    Attribute,
    form=AttributeForm,
    extra=1,  # Start with one empty form
    can_delete=True  # Allow deletion of attributes
)