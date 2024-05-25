from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

from .models import Registers
from passlib.hash import pbkdf2_sha256

def register(request):
	if request.method == 'POST':
		if request.POST.get('username') and request.POST.get('password1') and request.POST.get('password2'):
 
			inregistrare = Registers()
			inregistrare.username = request.POST.get('username')

			password = request.POST.get('password1')
			enc_password = pbkdf2_sha256.encrypt(password, rounds=12000,salt_size=32)
			inregistrare.password = enc_password

			usernames_list=[]
			usernames_list_db = Registers.objects.all().values_list()
			for i in range(len(usernames_list_db)):
				usernames_list.append(usernames_list_db[i][1])

			if request.POST.get('username') not in usernames_list:
				
				if request.POST.get('password1') == request.POST.get('password2'):
					
					inregistrare.save()
				else:
					return render(request, 'register/pass_not_match.html')
			else:
				return render(request, 'register/username_already_taken.html')
		return HttpResponseRedirect('/login/')
	else:
		request.session['username'] = 'logged out'
		return render(request, 'register/register.html')

#if pbkdf2_sha256.verify(password, enc_password) == True:
#				print("good")
			