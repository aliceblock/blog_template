from django import forms

from models import Comment

class CommentForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}), required=False)
    website = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}), required=False)
    text = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control'}))

    class Meta:
        model = Comment
        exclude = ['entry']