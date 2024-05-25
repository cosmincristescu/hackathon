from django.shortcuts import render

from register.models import Registers
from django.http import HttpResponseRedirect
from passlib.hash import pbkdf2_sha256
from django.contrib import messages

def login_page(request):

	
	if request.method == 'POST':
		
		usernames_list=[]
		passwords_list=[]
		usernames_list_db = Registers.objects.all().values_list()
		for i in range(len(usernames_list_db)):
			usernames_list.append(usernames_list_db[i][1])
			passwords_list.append(usernames_list_db[i][2])
		
		if request.POST.get('username') in usernames_list:
			index_username = usernames_list.index(request.POST.get('username'))

			hashed_password = passwords_list[index_username]
			input_password = request.POST.get('password')
			verify_password = pbkdf2_sha256.verify(input_password, hashed_password)
			
			if verify_password == True:	
				request.session['username'] = request.POST.get('username')	
				return HttpResponseRedirect('/home/')
			else:
				return render(request, 'register/invalid_username.html')
		else:
			return render(request, 'register/invalid_username.html')
		
	else:
		request.session['username'] = 'logged out'
		return render(request, 'persfin/login.html')
