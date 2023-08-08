from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('', views.LeadView)

urlpatterns = [
    path('api/', include(router.urls)),
    #path('crm-leads',views.crm_leads, name = 'crm-leads'),
    path('', views.index, name="CRM Home"),
    path('search/', views.lead_search),
    path('leads/<int:id>/', views.lead_details),
    path('add-followup/<int:id>/', views.add_followup),
    path('set-reminder/<int:id>/', views.set_reminder),
    path('set-site-visit/<int:id>/', views.set_site_visit),
    path('booking/<int:id>/', views.booking),
    path('login/', views.login_function),
    path('logout/', views.logout_function),
    path('incentives/', views.incentives),
    path('add-project/<int:id>/', views.add_project),
    path('site-visit-done/<int:id>/', views.site_visit_done),
    # 
    path('add-lead/', views.add_lead),
    path('filter-leads/', views.filter_leads),
    path('todays-followups/', views.todays_followus),
    path('webhook214/', views.webhook214, name="webhook214"),
]
