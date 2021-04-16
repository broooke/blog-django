from django import forms
from blog.models import Comment


class addCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)