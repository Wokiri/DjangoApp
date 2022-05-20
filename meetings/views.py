from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.views.generic import ListView
from django.contrib.auth.forms import UserCreationForm 
from django.db.models import Q

from .models import (
    OrganizationMember,
)
# from .forms import MembersForm

class HomeView(TemplateView):
    template_name = 'meetings/home_page.html'


class MembersView(ListView):
    template_name = 'meetings/members.html'
    context_object_name = 'organization_members'
    paginate_by = 25

    def get_queryset(self):
        return OrganizationMember.objects.order_by('date_joined')
        
