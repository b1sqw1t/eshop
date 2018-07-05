from django import forms

class search_form(forms.Form):
    input_search_text = forms.CharField(max_length=40)
