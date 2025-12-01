
from django import forms
from .models import SearchKeywords

"""
class SearchKeywordsForm(forms.ModelForm):
    class Meta:
        model = SearchKeywords
        fields = ['keywords']
"""

class SearchKeywordsForm(forms.Form):
    keywords = forms.CharField(label="keywords", max_length=20)
    