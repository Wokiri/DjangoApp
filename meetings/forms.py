from django import forms
from django.core.exceptions import ValidationError

from .models import (
    Meeting,
)



# class MembersForm(forms.ModelForm):
    
    
#     class Meta:
#         model = OrganizationMember
#         fields = (
#             'name',
#             'number',
#             'description',
#             'hold_type',
#             'occupancy',
#             'thumbnail_img',
#         )