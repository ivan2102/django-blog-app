from django import forms
from django.utils.translation import gettext_lazy as _
from posts.models import Comments, Subscribe


class CommentsForm(forms.ModelForm):
    class Meta:
        model =  Comments
        fields = {'content', 'email', 'name', 'website'}


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs['placeholder'] = 'Type your comment here...'
        self.fields['name'].widget.attrs['placeholder'] = 'Your Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Your Email'
        self.fields['website'].widget.attrs['placeholder'] = 'Website(optional)'


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscribe
        fields = { 'email' }
        labels = {'email': _('')}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'Enter your email'