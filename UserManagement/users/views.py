from django.shortcuts import render
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import SignUpForm,LoginForm
from django.contrib.auth.models import User
from .models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.forms import PasswordResetForm
from .forms import CustomPasswordResetForm,CustomSetPasswordForm,AccountVerificationForm
from django.contrib.auth.views import PasswordResetConfirmView,PasswordResetDoneView
from django.contrib.auth.views import PasswordResetCompleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail,EmailMessage
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.urls import reverse_lazy


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Create a user object but don't save it yet
            # Print the user details for debugging
            print(f"User: {user.username}")
            user.save()  # Save the user object
            return HttpResponseRedirect('/users/login/')  
        else:
            messages.error(request, 'Please correct the errors in the form.')  # Custom error message
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
def user_list(request):
    users = User.objects.all()  # Retrieve all users from the database
    return render(request, 'user_list.html', {'users': users})
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/users/account-verification/')  # Replace 'home' with the URL name of your home page
            else:
                form.add_error(None, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required 
def home(request):
    return render(request, 'home.html')

def reset_password(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            
            # Generate password reset token
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Build password reset URL
            # current_site = get_current_site(request)
            # reset_url = f"{current_site.domain}/password-reset/confirm/{uid}/{token}/"
            
            # # Render password reset email template
            # email_subject = 'Reset your password'
            # email_message = render_to_string('password_reset_email.html', {
            #     'reset_url': reset_url,
            #     'user': user,
            # })
            
            # # Send password reset email
            # # send_mail(email_subject, email_message, settings.DEFAULT_FROM_EMAIL, [email])
            # email = EmailMessage(email_subject, email_message, to=[user.email])
            
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            # reset_password_url = request.build_absolute_uri('password-reset/confirm/{uidb64}/{token}/')
            # reset_password_url = request.build_absolute_uri(reverse('MyPasswordResetConfirmView', kwargs={'uidb64': uidb64, 'token': token}))

            # Create the email message
            email_subject = 'Password Reset'
            email_message = email_message = render_to_string('password_reset_email.html', {
                'reset_url': 'http://127.0.0.1:8000/users/password-reset/confirm/{uidb64}/{token}/',
                'user': user,
            })
            email = EmailMessage(email_subject, email_message, to=[user.email])
            email.content_subtype = 'html' 
            email.send()
            # Redirect to password reset done page
            return render(request,'password_reset_done.html')
    else:
        form = CustomPasswordResetForm()
    
    context = {'form': form}
    return render(request, 'reset_password.html', context)

class MyPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    form_class = CustomSetPasswordForm
    success_message = "Your password has been reset successfully."
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = self.get_user()
        if user is not None:
            new_password = form.cleaned_data['new_password1']
            user.set_password(new_password)
            user.save()
            return super().form_valid(form)
        return render(self.request, self.template_name, {'form': form})
class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'
def account_verification(request):
    if request.method == 'POST':
        form = AccountVerificationForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the current user
            user = request.user

            # Update the user model fields with the form data
            user.NID_or_passport_number = form.cleaned_data['NID_or_passport_number']
            user.document_image = form.cleaned_data['document_image']

            # Save the user model
            user.save()

            # Redirect to a success page or perform any additional actions
            return redirect('verification_success')

    else:
        form = AccountVerificationForm()

    return render(request, 'account_verification.html', {'form': form})
def verification_success(request):
    return render(request, 'verification_success.html')