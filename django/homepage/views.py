from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import income, expense
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from openai import AzureOpenAI

# OpenAI API credentials
OPENAI_API_KEY = 'ca49bfed37b54f439deae2ef7c75bb63'

def get_openai_response(prompt):
	client = AzureOpenAI(
		azure_endpoint="https://smartmoneyai.openai.azure.com/",
		api_key="ca49bfed37b54f439deae2ef7c75bb63",
		api_version="2024-02-01"
	)

	response = client.chat.completions.create(
		model="Test",
		messages=[
			{"role": "system", "content": "You are a helpful assistant."},
			{"role": "user", "content": prompt}
		]
	)

	return response.choices[0].message.content

def homepage(request):
	if request.session['username'] == 'logged out':
		return HttpResponseRedirect('/login/')
	else:
		if request.method == "POST":
			if 'prompt' in request.POST:
				prompt = request.POST.get('prompt')
				ai_response = get_openai_response(prompt)
				context = {
					'ai_response': ai_response,
					'total_income': 0,
					'total_expense': 0,
					'balance': 0,
				}
				return render(request, 'homepage/dashboard.html', context)
			elif request.POST.get('what_earned') and request.POST.get('amount_earned') and request.POST.get('date_earned'):
				castig = income()
				castig.username_earned = request.session['username']
				castig.what_earned = request.POST.get('what_earned').upper()
				castig.amount_earned = request.POST.get('amount_earned')
				castig.date_earned = request.POST.get('date_earned')
				castig.message_earned = request.POST.get('message_earned')

				castig.save()
				return HttpResponseRedirect('/home/')
			elif request.POST.get('what_expense') and request.POST.get('amount_expense') and request.POST.get('date_expense'):
				cheltuiala = expense()
				cheltuiala.username_expense = request.session['username']
				cheltuiala.what_expense = request.POST.get('what_expense').upper()
				cheltuiala.amount_expense = request.POST.get('amount_expense')
				cheltuiala.date_expense = request.POST.get('date_expense')
				cheltuiala.message_expense = request.POST.get('message_expense')

				cheltuiala.save()

				scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

				basedir = os.path.abspath(os.path.dirname(__file__))
				data_json = basedir + '/Test-ec10a3a14e27.json'
				credentials = ServiceAccountCredentials.from_json_keyfile_name(data_json, scope)

				gc = gspread.authorize(credentials)

				wks = gc.open('Personal Finance').sheet1

				wks.append_row(['', '', '', '',
								request.POST.get('date_expense'),
								request.POST.get('what_expense').upper(),
								request.POST.get('amount_expense')])

				return HttpResponseRedirect('/home/')
			else:
				return HttpResponseRedirect('/home/')
		else:
			total_income = sum(income.objects.filter(username_earned=request.session['username']).values_list('amount_earned', flat=True))
			total_expense = sum(expense.objects.filter(username_expense=request.session['username']).values_list('amount_expense', flat=True))
			balance = total_income - total_expense

			income_balance_expense = {
				'total_income': total_income,
				'total_expense': total_expense,
				'balance': balance
			}
			return render(request, 'homepage/dashboard.html', income_balance_expense)

def income_history(request):
	if request.session['username'] == 'logged out':
		return HttpResponseRedirect('/login/')
	else:
		income_list_db = income.objects.filter(username_earned=request.session['username']).values_list()
		length_income = len(income_list_db)

		what_earned_list = []
		for index in range(length_income):
			what_earned_list.append(income_list_db[index][2])

		date_earned_list = []
		for index in range(length_income):
			date_earned_list.append(income_list_db[index][4])

		amount_earned_list = []
		for index in range(length_income):
			amount_earned_list.append(income_list_db[index][3])

		message_earned_list = []
		for index in range(length_income):
			message_earned_list.append(income_list_db[index][5])

		fusion = zip(what_earned_list, date_earned_list, amount_earned_list, message_earned_list)
		income_dictionary = {
			"fusion": fusion
		}

		return render(request, 'homepage/income_history.html', income_dictionary)

def expenses_history(request):
	if request.session['username'] == 'logged out':
		return HttpResponseRedirect('/login/')
	else:
		expense_list_db = expense.objects.filter(username_expense=request.session['username']).values_list()
		length_expense = len(expense_list_db)

		what_expense_list = []
		for index in range(length_expense):
			what_expense_list.append(expense_list_db[index][2])

		date_expense_list = []
		for index in range(length_expense):
			date_expense_list.append(expense_list_db[index][4])

		amount_expense_list = []
		for index in range(length_expense):
			amount_expense_list.append(expense_list_db[index][3])

		message_expense_list = []
		for index in range(length_expense):
			message_expense_list.append(expense_list_db[index][5])

		fusion = zip(what_expense_list, date_expense_list, amount_expense_list, message_expense_list)
		expense_dictionary = {
			"fusion": fusion
		}
		return render(request, 'homepage/expenses_history.html', expense_dictionary)

def settings(request):
	if request.session['username'] == 'logged out':
		return HttpResponseRedirect('/login/')
	else:
		if request.method == "POST":
			currency_used = '$'
			if request.POST.get('currency') == 'dollar':
				currency_used == '$'
			elif request.POST.get('currency') == 'pound':
				currency_used == '&#8356;'
			elif request.POST.get('currency') == 'euro':
				currency_used == '&#8364;'

		return render(request, 'homepage/settings.html')
