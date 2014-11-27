from django import forms

from models import Comment

class CommentForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}))
    website = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}))
    text = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control'}))

    class Meta:
        model = Comment
        exclude = ['entry']