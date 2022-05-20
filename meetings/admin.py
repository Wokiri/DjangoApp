from django.contrib import admin

from .models import (
    OrganizationMember,
    Meeting,
    MeetingAttendee,
    Agenda,
)

class OrganizationMemberAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'email',
        'role',
    )
    list_filter = (
        'role',
        'gender',
    )
    search_fields = [
        'first_name',
        'last_name',
        'email__exact',
    ]

class MeetingAdmin(admin.ModelAdmin):
    list_display = ('meeting_title',)
    search_fields = ['meeting_title']

class MeetingAttendeeAdmin(admin.ModelAdmin):
    list_display = (
        'organization_member',
        'present',
        'absent_with_apology',
        'absent_without_apology',
    )
    list_filter = (
        'present',
        'absent_with_apology',
        'absent_without_apology',
    )
    search_fields = ['organization_member']

class AgendaAdmin(admin.ModelAdmin):
    list_display = (
        'meeting',
        'title',
        'created',
    )
    search_fields = ['title']

admin.site.register(OrganizationMember, OrganizationMemberAdmin)
admin.site.register(Meeting, MeetingAdmin)
admin.site.register(MeetingAttendee, MeetingAttendeeAdmin)
admin.site.register(Agenda, AgendaAdmin)


