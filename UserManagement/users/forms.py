from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordResetForm,SetPasswordForm
from django.core.validators import FileExtensionValidator

class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name','last_name','username','email', 'password1', 'password2','gender', 'age', 'date_of_birth', 'marital_status', 'nationality')

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Password'})
class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label='Email', max_length=254)
# class MyPasswordResetConfirmForm(SetPasswordForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['new_password1'].widget.attrs.update({'placeholder': 'new password'})
#         self.fields['new_password2'].widget.attrs.update({'placeholder': 'confirm password'})
class CustomSetPasswordForm(SetPasswordForm):

      def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs['placeholder'] = 'New Password'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm New Password'
class AccountVerificationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['NID_or_passport_number', 'document_image']
        document_image = forms.ImageField(
    validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
)
