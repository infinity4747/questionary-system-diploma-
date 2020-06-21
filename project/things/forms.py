from django import forms
from django.forms import ModelForm
from .models import Student
from django.core.exceptions import ValidationError
class StudentLoginForm(forms.Form):
    id = forms.CharField(label='Your name', max_length=100)
    def clean_id(self):
        id_input = self.cleaned_data['id']
        # print(Student.objects.filter(id__iexact=id_input).count())
        if Student.objects.filter(id__iexact=id_input).count() == 0:
            raise ValidationError("Incorect id,please check your id")
        return id_input
class PhotoForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('photo',)