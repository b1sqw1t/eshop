from django import forms
from django.forms import ModelForm, Textarea
from comments.models import Comment

class comments_form(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('Text','Product','User')
        widgets = {'Product': forms.HiddenInput(),
                   'User': forms.HiddenInput(),
                   'Text': Textarea(attrs={'cols': 86, 'rows': 6})}
