from django.urls import path

from .views import (
    HomeView,
    MembersView,
)

app_name = 'meetings'

urlpatterns = [
    path('', HomeView.as_view(), name='home_page'),
    path('members/', MembersView.as_view(), name='members_page'),
]