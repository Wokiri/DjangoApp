from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.urls import reverse

from .manager import CustomUserManager

import uuid


class GENDER(models.TextChoices):
    MALE = 'Male', _('Male')
    FEMALE = 'Female', _('Female')


class ROLE(models.TextChoices):
    CHAIRPERSON = 'Chairperson', _('Chairperson')
    SECRETARY = 'Secretary', _('Secretary')
    TREASURER = 'Treasurer', _('Treasurer')
    MEMBER = 'Member', _('Member')


class OrganizationMember(AbstractUser):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=11, choices=ROLE.choices, default=ROLE.MEMBER)
    gender = models.CharField(max_length=6, choices=GENDER.choices)
    thumbnail = models.ImageField(upload_to='thumbnails/', default='default_avatar.png') # Img in media
    date_joined = models.DateField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    username = None

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Organization member'
        verbose_name_plural = verbose_name + 's'

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)
        
    def get_absolute_url(self):
        return reverse('meetings:member', kwargs={'slug' : self.slug})

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()
        

class Meeting(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    meeting_title = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.meeting_title

    class Meta:
        ordering = ['-date']


class MeetingAttendee(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    organization_member = models.OneToOneField(OrganizationMember, on_delete=models.CASCADE)
    meeting = models.ManyToManyField(Meeting, related_name='meeting_attendees')
    present = models.BooleanField(default=True)
    absent_with_apology = models.BooleanField(default=False)
    absent_without_apology = models.BooleanField(default=False)

    def clean(self):
        if self.present and any([self.absent_with_apology, self.absent_without_apology]):
            raise ValidationError(_('A member cannot at the same time be present and absent'))

        if all([self.absent_with_apology, self.absent_without_apology]):
            raise ValidationError(_('A member cannot at the same time be absent with apology and without apology'))

    def __str__(self):
        return '%s %s' % (self.organization_member.first_name, self.organization_member.last_name)


class Agenda(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    meeting = models.ForeignKey(Meeting, related_name='meeting_agenda', on_delete=models.CASCADE)
    title = models.CharField(max_length=125)
    description = models.TextField()
    concerned_members = models.ManyToManyField(OrganizationMember, related_name='concerned_members')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Agendanum'
        verbose_name_plural = 'Agenda'
        ordering = ['-created']