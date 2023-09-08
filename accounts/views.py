
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Account
from .forms import RegistrationForm

# Create your views here.
def register(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      first_name = form.cleaned_data['first_name']
      last_name = form.cleaned_data['last_name']
      email = form.cleaned_data['email']
      phone_number = form.cleaned_data['phone_number']
      password = form.cleaned_data['password']
      username = email.split('@')[0]

      user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
      user.phone_number = phone_number
      user.save()
      return redirect('register')
    else:
      messages.error(request=request, message="Register failed!")
  else:
    form = RegistrationForm()
  context = {
    'form': form,
  }
  return render(request, 'accounts/register.html', context=context)