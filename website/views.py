from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	return render(request, 'website/index.html')

def about(request):
	return render(request, 'website/about.html')

def contact(request):
	return render(request, 'website/contact.html')

def properties(request):
	return render(request, 'website/properties.html')

def partners(request):
	return render(request, 'website/partners.html')

def privacy(request):
        return render(request, 'website/privacy.html')

def terms(request):
        return render(request, 'website/terms.html')

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
