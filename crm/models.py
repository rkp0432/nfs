from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.utils import timezone
class Staff(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	phone = models.CharField(max_length=15)
	team = models.CharField(max_length=60,
		choices = (
			('Management', 'Management'),
			('WorkHorse', 'WorkHorse'),
			),
		default = "WorkHorse"
		)
	date_created = models.DateField(auto_now_add=True)
	date_modified = models.DateField(auto_now=True)
	def __str__(self):
		return "%s" % self.user.username

class Lead(models.Model):
	name = models.CharField(max_length=200)
	phone = models.CharField(max_length=20)
	facebook_id = models.CharField(max_length=200, unique=True, default=timezone.now())
	alt_phone = models.CharField(max_length=20, null=True, blank=True)
	email = models.EmailField(null=True, blank=True)
	project_name = models.CharField(max_length=200, null=True, blank=True)
	project_location = models.CharField(max_length=30, 
		choices = (
			('East', 'East'),
			('West', 'West'),
			('North', 'North'),
			('South', 'South'),
			('CBD', 'CBD'),
			),
		null = True,
		blank = True,
		verbose_name="Project Location"
		)
	project_type = models.CharField(max_length=30,
		choices = (
			('Apartment', 'Apartment'),
			('Villa', 'Villa'),
			('Plot', 'Plot'),
			('Resale', 'Resale'),
			('Commercial', 'Commercial'),
			),
		null = True,
		blank = True,
		verbose_name="Project Type"
		)
	project_completion_status = models.CharField(max_length=30,
		choices = (
			('Pre-launch', 'Pre-launch'),
			('Under Construction', 'Under Construction'),
			('Ready to move', 'Ready to move'),
			),
		null = True,
		blank = True,
		verbose_name = "Project Completion"
		)
	budget = models.CharField(max_length=30,
		choices = (
			('Upto 50 lakh', 'Upto 50 lakh'),
			('50 lakh - 1 crore', '50 lakh - 1 crore'),
			('1 crore - 2 crore', '1 crore - 2 crore'),
			('2 crore - 3 crore', '2 crore - 3 crore'),
			('3 crore - 5 crore', '3 crore - 5 crore'),
			('Above 5 crore', 'Above 5 crore'),
			),
		null = True,
		blank = True,
		)
	source = models.CharField(max_length=30, 
		choices = (
			('Facebook', 'Facebook'),
			('Google', 'Google'),
			('Reference', 'Reference'),
			('CommonFloor', 'CommonFloor'),
			('Other', 'Other'),
			),
		default = 'Reference'
		)
	duplicate_lead = models.BooleanField(default=False)
	date_of_enquiry = models.DateField(auto_now_add=True)
	date_modified = models.DateField(auto_now=True)
	status = models.CharField(max_length=30, 
		choices = (
			('Open', 'Open'),
			('Hot', 'Hot'),
			('Warm', 'Warm'),
			('Cold', 'Cold'),
			('Postpone', 'Postpone'),
			('Dropped', 'Dropped'),
			('Invalid', 'Invalid'),
			('Booking', 'Booking'),
			),
		default = "Open",
		)
	initial_observation = models.TextField(blank=True, null=True)

	def lead_details(self):
		return format_html('''
			<span style="color:#777;font-weight:600">{}</span><br>
			<span style="color:#660066;font-weight:600">{}</span><br>
			<span style="color:#294f75;font-weight:600">{}</span><br>
			<span style="color:#660066;font-weight:600">{}</span><br>
			''', self.name, self.phone, self.email, self.date_of_enquiry)

	def project_details(self):
		return format_html('''
			<span style="color:#777;font-weight:600">{}</span><br>
			<span style="color:#660066;font-weight:600">{}</span> | 
			<span style="color:#294f75;font-weight:600">{}</span><br>
			<span style="color:#294f75;font-weight:400">{}</span><br>
			<span style="color:#294f75;font-weight:400">{}</span><br>
			''', self.project_name, self.project_location, self.project_type, self.project_completion_status, self.budget)
	
	# Assign
	assigned_to = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)
	
	# Booking
	unit_number = models.CharField(max_length=60, null=True, blank=True)
	agreement_value = models.PositiveIntegerField(default=0)
	booking_date = models.DateField(auto_now=True)
	
	# Reward 
	nfs_brokerage = models.FloatField(default=0)
	cashback = models.FloatField(default=0)
	staff_brokerage = models.FloatField(default=0)
	
	# Brokerage Amounts
	def nfs_brokerage_value(self):
		return (self.agreement_value-self.cashback)*self.nfs_brokerage/100
	def staff_brokerage_value(self):
		return ((self.agreement_value-self.cashback)*self.nfs_brokerage/100)*self.staff_brokerage/100
	
	# Remider
	reminder = models.DateField(null=True, blank=True, verbose_name="Set Reminder For")
	
	# Site visit
	site_visit_fixed = models.BooleanField(default=False, verbose_name="S.V")
	site_visit_done = models.BooleanField(default=False)
	site_visit_date = models.DateField(null=True, blank=True)
	
	# Followup remarks 
	last_followup_remarks = models.TextField(blank=True, null=True)
	
	def __str__(self):
		return self.name

class Followup(models.Model):
	lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
	timestamp = models.DateField(auto_now_add=True)
	followup_remarks = models.TextField()
	by = models.CharField(max_length=60, blank=True, null=True)
