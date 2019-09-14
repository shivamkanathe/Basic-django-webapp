from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login ,logout,authenticate
from django.contrib import messages
from .forms import NewUserForm



def homepage(request):
	return render(request=request,
		         template_name="main/index.html")



def register(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			messages.success(request,f"new account created {username}")
			login(request,user)
			messages.info(request,f"you are logged in as {username}" )
			return redirect("main:homepage")
		else:
			for msg in form.error_messages:
				print(form.error_messages[msg])	

	form = NewUserForm
	return render(request,
		         "main/register.html",
		         context={"form":form})	

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request,data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username,password=password)

			if user is not None:
				login(request,user)
				messages.info(request,f"you are now logged in")
				return redirect("main:homepage")
			else:
				messages.error(request,f"invalid username or password")
		else:
			messages.error(request,f"invalid username or password")		


	form = AuthenticationForm()
	return render(request,
		         "main/login.html",
		         context={"form":form})	

def logout_request(request):
	logout(request)
	messages.info(request,f"you are logged out")
	return redirect("main:homepage")	



	