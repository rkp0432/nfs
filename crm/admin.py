from .models import *
from django.db import models
from django.contrib import admin
from django.forms import TextInput, Textarea 
from import_export.admin import ImportExportModelAdmin
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter
from django.contrib.auth.models import Group

admin.site.site_header = "Next Footstep"
admin.site.index_title = "CRM"



# **************** Lead & Followup ******************

class FollowupInline(admin.TabularInline):
	model = Followup
	extra = 0
	exclude = ['by',]
	def has_delete_permission(self, request, obj=None): return False
	formfield_overrides = {
		models.TextField: {'widget': Textarea(attrs={'rows':'3', 'cols':80})},
	}
	readonly_fields = ('timestamp',)
	fieldsets = (
		(None, {
			'fields': (
				('followup_remarks',),
				)
			}),
		)

class LeadAdmin(ImportExportModelAdmin, admin.ModelAdmin):
	inlines = [FollowupInline]
	search_fields = ['id', 'name', 'phone', 'project_name']
	formfield_overrides = {
		models.DateField: {'widget': TextInput(attrs={'size':'50'})},
		models.CharField: {'widget': TextInput(attrs={'size':'50'})},
		models.EmailField: {'widget': TextInput(attrs={'size':'50'})},
		models.TextField: {'widget': Textarea(attrs={'rows':'3', 'cols':133})},
	}
	readonly_fields = ('date_of_enquiry', 'date_modified')
	fieldsets = (
		(
		None, {
			'fields':(
				('date_of_enquiry',),
				('name', 'phone',), 
				('email', 'project_name'),
				('project_location', 'project_type',),
				('project_completion_status', 'budget'),
				('status',),
				('initial_observation',)
				),
			},
		),
		(
            "Booking Details",
            {
                "classes": ["collapse"],
                "fields": ["unit_number", "agreement_value"],
            },
        ),
		(
            "Brokerage",
            {
                "classes": ["collapse"],
                "fields": ["nfs_brokerage", "cashback", "staff_brokerage"],
            },
        ),
	)
	list_display = ['id', 'lead_details', 'project_details', 'initial_observation', 'status', 'site_visit_fixed', 'assigned_to']
	list_display_links = ['status']
	list_filter = (
		'assigned_to',
        ('status', ChoiceDropdownFilter),
        ('project_location', ChoiceDropdownFilter),
        ('project_type', ChoiceDropdownFilter),
        ('budget', ChoiceDropdownFilter),
        ('project_completion_status', ChoiceDropdownFilter),
        ('site_visit_done', DropdownFilter),
        ('project_name', ChoiceDropdownFilter),
        )
	list_editable = ['id', 'assigned_to']
	ordering = ['-id']
	date_hierarchy = 'date_of_enquiry'
	list_per_page = 50

admin.site.register(Lead, LeadAdmin)






# **************** Staff ******************

class StaffAdmin(admin.ModelAdmin):
	list_display = ['id', 'user', 'phone', 'team']
	search_fields = ['phone']

admin.site.register(Staff, StaffAdmin)






# ****************** Activity Logger ******************

from django.contrib.admin.models import LogEntry, DELETION
from django.utils.html import escape
from django.urls import reverse
from django.utils.safestring import mark_safe

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'

    list_filter = [
        'user',
        'content_type',
        'action_flag'
    ]

    search_fields = [
        'object_repr',
        'change_message'
    ]

    list_display = [
        'action_time',
        'user',
        'content_type',
        'object_link',
        'action_flag',
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = '<a href="%s">%s</a>' % (
                reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id]),
                escape(obj.object_repr),
            )
        return mark_safe(link)
    object_link.admin_order_field = "object_repr"
    object_link.short_description = "object"
