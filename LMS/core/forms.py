from django import forms
from .models import Users, Question, Attribute, Test, ClassGroup
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


class TestForm(forms.ModelForm):
    classGroup = forms.ModelChoiceField(
        queryset=ClassGroup.objects.none(), 
        label="Class Group", 
        required=True
    )

    class Meta:
        model = Test
        fields = ['test_name', 'level', 'age', 'type', 'questions_no', 'questions_dif', 'classGroup']

    def __init__(self, *args, **kwargs):
        professor = kwargs.pop('professor', None)
        super(TestForm, self).__init__(*args, **kwargs)
        
        if professor:
            self.fields['classGroup'].queryset = ClassGroup.objects.filter(professors=professor).order_by('class_name')
            self.fields['classGroup'].widget = forms.Select(choices=[(group.gid, group.class_name) for group in self.fields['classGroup'].queryset])