from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
from django.db.models import Q
from django.core.paginator import Paginator
from datetime import date
import json
from rest_framework import viewsets
from .serializers import LeadSerializer
class LeadView(viewsets.ModelViewSet):
	queryset = Lead.objects.all()
	serializer_class = LeadSerializer
from django.views.decorators.csrf import csrf_exempt

def crm_leads(request): ...


# webhook
@csrf_exempt
def webhook214(request):
	access_token = "EAAIETM1TdZCoBOyd7PHZByCdrziuZBn1XXIbbZBi7mg6sG5kZAArKNpPOZAzZC6LwhWcGcg43ZA898ZAkiBKxtCH0LhIb20LSaoZBjTinfKbZC9wgMjR0MrMlAZCMbAIryyP8KvBNglUpZBdZCvTuZCBzEmqYt9TziYr1JfOSzplre6sWI0apNgnZBiwaluq3UzlDA6QCv3ZBvAuqvvtcAx9ATLsZD"

	# print(request.body)
	res = json.loads(request.body)
	print("res")
	print(res)
	# print(res['entry'])
	# print(res['entry'][0])
	
	# print(res['entry'][0]['id'])
	
	# print(res['entry'][0]['changes'][0]['value'])
	# print("form_id ", res['entry'][0]['changes'][0]['value']['form_id'])
	# print("leadgen_id ", res['entry'][0]['changes'][0]['value']['leadgen_id'])
	# print("page_id ", res['entry'][0]['changes'][0]['value']['page_id'])

	form_id = res['entry'][0]['changes'][0]['value']['form_id']
	leadgen_id = res['entry'][0]['changes'][0]['value']['leadgen_id']
	# print("form_id",form_id)
	# print("leadgen_id",leadgen_id)

	url_leads_p = "https://graph.facebook.com/v17.0/"+str(form_id)+"?access_token="+str(access_token)
	# print(url_leads_p)
	payload_leads_p = {}
	headers_leads_p = {
		'Content-Type': 'application/json'
		}
	response_leads_p = requests.request("GET", url_leads_p, headers=headers_leads_p, data=payload_leads_p)
	# print("project")
	# print(response_leads_p.text)
	project = json.loads(response_leads_p.text)
	project_name = project['name']
	
	url_leads = "https://graph.facebook.com/v17.0/"+str(leadgen_id)+"?access_token="+str(access_token)
	payload_leads = {}
	headers_leads = {
		'Content-Type': 'application/json'
		}
	response_leads = requests.request("GET", url_leads, headers=headers_leads, data=payload_leads)
	# print(response_leads.text)
	lead = json.loads(response_leads.text)
	count= 0
	
	# created_time = lead['created_time']
	facebook_lead_id = lead['id']
	# print("facebook_lead_id", facebook_lead_id)
	if lead['field_data'][0]['name'] == 'full_name':
		name = lead['field_data'][0]['values']
	if lead['field_data'][0]['name'] == 'phone_number':
		phone_number = lead['field_data'][0]['values']
	if lead['field_data'][0]['name'] == 'email':
		email = lead['field_data'][0]['values']
	
	if lead['field_data'][1]['name'] == 'full_name':
		name = lead['field_data'][1]['values']
	if lead['field_data'][1]['name'] == 'phone_number':
		phone_number = lead['field_data'][1]['values']
	if lead['field_data'][1]['name'] == 'email':
		email = lead['field_data'][1]['values']

	if lead['field_data'][2]['name'] == 'full_name':
		name = lead['field_data'][2]['values']
	if lead['field_data'][2]['name'] == 'phone_number':
		phone_number = lead['field_data'][2]['values']
	if lead['field_data'][2]['name'] == 'email':
		email = lead['field_data'][2]['values']

	# print(name,email,phone_number, project_name)

	# try:
		
	url_next_foot = "https://www.nextfootstep.in/crm/api/"
	# print(url_leads)
	payload_next_foot = json.dumps({
		"email": email[0],
		"name": name[0],
		"phone":phone_number[0],
		"project_name":project_name,
		"facebook_id":facebook_lead_id
		})
	# print(payload_next_foot)
	headers_next_foot = {
		'Content-Type': 'application/json'
	}
	# payload_next_foot = {"id":5065,"name":"PREM sooli maga","phone":"+919901762218","email":"sharmila.a@livprotec.com","project_name":"Auto_ITQE","facebook_id":"846848833531969"}
	response_leads = requests.request("POST", url_next_foot, headers=headers_next_foot, data=payload_next_foot)
	print("response_leads=",response_leads.text)
		# Leads.objects.create(name=name,phone=phone_number, email=email, facebook_id=facebook_lead_id)
	# except:
	# 	pass

	hub_challange = request.GET.get('hub.challenge')
	hub_mode = request.GET.get('hub.mode')
	hub_verify_token = request.GET.get('hub.verify_token')


	if hub_verify_token == 'abcdefghijklmn0123456789':
		return HttpResponse(hub_challange)
	else:
		return HttpResponse(False)



@login_required
def index(request):
	try:
		staff_id = Staff.objects.get(user=request.user.id)
		my_leads = Lead.objects.filter(assigned_to=staff_id, status__in=['Open', 'Hot', 'Warm', 'Cold']).order_by('-id')
	except:
		my_leads = Lead.objects.filter(status = 'Open')
	p = Paginator(my_leads, 50)
	try:
		page_number = request.GET.get('page')
		page_object = p.page(page_number)
	except:
		page_object = p.page(1)
	return render(request, 'crm/index.html', {'my_leads':page_object})

@login_required
def todays_followus(request):
	try:
		staff_id = Staff.objects.get(user=request.user.id)
		my_leads = Lead.objects.filter(Q(reminder=date.today(), assigned_to=staff_id) | Q(site_visit_date=date.today(), assigned_to=staff_id)).order_by('-id')
	except:
		my_leads = Lead.objects.filter(Q(reminder=date.today()) | Q(site_visit_date=date.today())).order_by('-id')
	p = Paginator(my_leads, 50)
	try:
		page_number = request.GET.get('page')
		page_object = p.page(page_number)
	except:
		page_object = p.page(1)
	return render(request, 'crm/todays_followups.html', {'my_leads':page_object})


@login_required
def lead_details(request, id):
	selected_lead = Lead.objects.get(id=id)
	followups = Followup.objects.filter(lead=selected_lead)
	return render(request, 'crm/lead_details.html', {
		'selected_lead':selected_lead, 
		'followups':followups,
		})

@login_required
def lead_search(request):
	phone = request.GET.get('phone').strip()
	selected_lead = Lead.objects.filter(phone=phone).first()
	if selected_lead:
		followups = Followup.objects.filter(lead=selected_lead)
		return render(request, 'crm/lead_search.html', {
			'selected_lead':selected_lead, 
			'followups':followups,
			})
	else:
		return HttpResponse("""
			<p>No result found.<br>
			<a href="/">click here</a> to try again.
			""")

@login_required
def add_followup(request, id):
	if request.method=="POST":
		new_followup = Followup.objects.create(
			lead=Lead.objects.get(id=id), 
			followup_remarks=request.POST['followup_remarks'],
			by=request.user.username,
			)
		new_followup.save()
		Lead.objects.filter(id=id).update(status=request.POST['status'], initial_observation=request.POST['followup_remarks'])
		return redirect('/crm/')
	else:
		return HttpResponse("Access denied")

@login_required
def set_reminder(request, id):
	if request.method=="POST":
		selected_lead = Lead.objects.filter(id=id)
		reminder_input_value= request.POST['reminder']
		reminder_input_value.split("-").reverse()
		selected_lead.update(reminder=reminder_input_value)
		return redirect("/crm/")
	else:
		return HttpResponse("Access denied")

@login_required
def set_site_visit(request, id):
	if request.method=="POST":
		selected_lead = Lead.objects.filter(id=id)
		sv_input_value= request.POST['site_visit_date']
		sv_input_value.split("-").reverse()
		selected_lead.update(site_visit_date=sv_input_value, site_visit_fixed=True)
		return redirect("/crm/")
	else:
		return HttpResponse("Access denied")

@login_required
def booking(request, id):
	if request.method=="POST":
		selected_lead = Lead.objects.filter(id=id)
		project_name = request.POST['project_name']
		unit_number = request.POST['unit_number']
		agreement_value = request.POST['agreement_value']
		selected_lead.update(
			project_name=project_name,
			unit_number=unit_number, 
			agreement_value=agreement_value, 
			status="Booking")
		return redirect("/crm/leads/%s" % id)
	else:
		return HttpResponse("Access denied")

def login_function(request):
	if request.method=="POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user:
			login(request, user)
			return redirect('/crm/')
		else:
			return HttpResponse("""
				<h3>Your username or password did not match. </h3>
				<br>
				<a href="/crm/login/">click here</a> to try again
				""")
	return render(request, 'crm/login.html', {})

@login_required
def logout_function(request):
	logout(request)
	return redirect('/')

@login_required
def incentives(request):
	try:
		staff_id = Staff.objects.get(user=request.user.id)
		leads = Lead.objects.filter(assigned_to=staff_id, status="Booking").order_by('-id')
	except:
		leads = Lead.objects.filter(status="Booking").order_by('-id')
	p = Paginator(leads, 50)
	try:
		page_number = request.GET.get('page')
		page_object = p.page(page_number)
	except:
		page_object = p.page(1)
	return render(request, 'crm/incentives.html', {'leads':page_object})

@login_required
def add_project(request, id):
	if request.method=="POST":
		selected_lead = Lead.objects.filter(id=id)
		project_name = request.POST['project_name'].title()
		project_location = request.POST['project_location']
		project_type = request.POST['project_type']
		project_completion_status = request.POST['project_completion_status']
		budget = request.POST['budget']
		selected_lead.update(
			project_name=project_name, 
			project_location=project_location,
			project_type=project_type,
			project_completion_status=project_completion_status,
			budget=budget
			)
		return redirect("/crm/leads/%s" % id)
	else:
		return HttpResponse("Access denied")

@login_required
def site_visit_done(request, id):
	if request.method=="POST":
		selected_lead = Lead.objects.filter(id=id)
		selected_lead.update(site_visit_done=True)
		return redirect("/crm/")
	else:
		return HttpResponse("Access denied")

@login_required
def add_lead(request):
	form = LeadForm(request.POST or None)
	if form.is_valid():
		new_lead = form.save(commit=False)
		new_lead.assigned_to = Staff.objects.get(user=request.user.id)
		new_lead.save()
		return redirect("/crm/")
	return render(request, 'crm/add-lead.html', {'form':form})

@login_required
def filter_leads(request, project_location=""):
	if request.method=="POST":
		staff_id = Staff.objects.get(user=request.user.id)
		result = Lead.objects.filter(assigned_to=staff_id)
		if 'status' in request.POST:
			result = result.filter(status=request.POST['status'])
		if 'project_location' in request.POST:
			result = result.filter(project_location=request.POST['project_location'])
		if 'project_type' in request.POST:
			result = result.filter(project_type=request.POST['project_type'])
		if 'project_completion_status' in request.POST:
			result = result.filter(project_completion_status=request.POST['project_completion_status'])
		if 'budget' in request.POST:
			result = result.filter(budget=request.POST['budget'])
		result.order_by('-id')
		return render(request, 'crm/index.html', {'my_leads':result})
	else:
		return redirect('/crm/')
