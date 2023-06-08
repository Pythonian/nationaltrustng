from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'
        self.fields['body'].widget.attrs = {'class': 'form-control text-area'}

    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']