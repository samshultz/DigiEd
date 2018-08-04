from django import forms


class SearchForm(forms.Form):
    q = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': "Search using book titles, publisher and authors"}))
