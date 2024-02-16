from django import forms

from .models import Reviews
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class ReviewForm(forms.ModelForm):
    """Форма отзывов"""

    class Meta:
        model = Reviews
        fields = ("name", "email", "text")


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ReviewForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['name'].initial = user.username
            self.fields['email'].initial = user.email

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError("Некорректный адрес электронной почты")
        return email
