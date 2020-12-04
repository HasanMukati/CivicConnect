from django import forms

def should_be_empty(value):
    if value:
        raise forms.ValidationError('Field is not empty')

class ContactForm(forms.Form):
    name = forms.CharField(max_length=80)
    # message = forms.CharField(widget = forms.Textarea)
    # email = forms.EmailField()
    recipient_email = forms.EmailField(widget = forms.Textarea(attrs={"rows":1,"cols":50}), max_length=200)
    forcefield = forms.CharField(
        required=False, widget=forms.HiddenInput, label="Leave empty", validators=[should_be_empty])

