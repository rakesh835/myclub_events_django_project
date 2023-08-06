from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import RegisterUserForm

# Create your views here.


def register_user(request):
	if request.method == 'POST':
		form = RegisterUserForm(request.POST)

		if form.is_valid():
			form.save(commit=False)
			username = form.cleaned_data.get('username')
			first_name = form.cleaned_data.get('first_name')
			last_name = form.cleaned_data.get('last_name')
			email = form.cleaned_data.get('email')
			password = form.cleaned_data.get('password1')
			user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
			messages.success(request, 'You are registered successfullyly.')
			return redirect('login')
		else:
			messages.warning(request, "Please enter valid credentials.")
			return render(request, 'accounts/register_user.html', {'form': form})
	
	else:
		form = RegisterUserForm()

	context = {
		'form': form,
	}	

	return render(request, 'accounts/register_user.html', context)



def login_user(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
	
		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			messages.success(request, 'Logged in successfully.')
			return redirect('my_events')
		else:
			messages.error(request, 'Invalid credentials. Try again.')
			return redirect('login')

	return render(request, 'accounts/login.html')



@login_required
def logout_user(request):
	logout(request)
	messages.success(request, 'Logged out succefully.')

	return redirect('home')