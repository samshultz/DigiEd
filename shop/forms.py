from django import forms
from django.contrib.auth.models import User

class SearchForm(forms.Form):
    q = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': "Search using book titles, publisher and authors"}))

class UserEditForm(forms.ModelForm):
    """Form definition for UserEdit."""

    class Meta:
        """Meta definition for UserEditform."""

        model = User
        fields = ('first_name', 'last_name', 'username')

    
