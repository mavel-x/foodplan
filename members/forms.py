from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from members.models import CustomUser
from django.contrib.auth import get_user_model, password_validation
from django.core.exceptions import ValidationError
from django import forms


class CreateUserForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["email"].widget.attrs["class"] = "form-control"
        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["class"] = "form-control"

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']


class ChangeUserForm(UserChangeForm):
    password1 = forms.CharField(required=False)
    password2 = forms.CharField(required=False)
    password = None

    def clean(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2:
            if password1 != password2:
                errors = {'password2': ValidationError('The two password fields didn\’t match.', code='password_mismatch')}
                raise ValidationError(errors)
            password_validation.validate_password(password1, self.instance)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', ]
