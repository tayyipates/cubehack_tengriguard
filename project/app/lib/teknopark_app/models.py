from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import datetime, timedelta, time
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email alanı zorunludur.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser is_staff=True olmalı.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser is_superuser=True olmalı.")

        return self.create_user(email, password, **extra_fields)



def upload_to_logo(instance, filename):
    return f'sirket_logolari/{instance.first_name}/{filename}'

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    uygunluk = models.BooleanField(default=True)
    sirket = models.CharField(max_length=120, null=True, blank=True)
    sirket_bilgileri = models.TextField(null=True, blank=True, max_length=500)
    web_adresi = models.URLField(blank=True, null=True)
    iletisim_emaili = models.EmailField(blank=True, null=True)
    sirket_logosu = models.ImageField(upload_to=upload_to_logo, blank=True, null=True)
    categories = models.ManyToManyField('Category', blank=True, related_name='users')

    ROLE_CHOICES = (
        ('investor', 'Yatırımcı'),
        ('entrepreneur', 'Girişimci'),
        ('teknopark', 'Teknopark'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    # Yeni eklenen alanlar
    yatirim_miktari = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.0'))],
        help_text="Yatırımcı isen, yatırım yapmayı düşündüğün miktar ($)"
    )
    talep_edilen_yatirim = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.0'))],
        help_text="Girişimci isen, talep ettiğin yatırım miktarı ($)"
    )
    THS_CHOICES = [(str(i), f"THS-{i} seviyesi") for i in range(1, 10)]

    ths = models.CharField(max_length=2, choices=THS_CHOICES, null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        if self.first_name or self.last_name:
            return f"{self.first_name or ''} {self.last_name or ''}".strip()
        return self.email

    def clean(self):
        super().clean()
        
        # Teknopark email kontrolü
        if self.role == 'teknopark' and not self.email.endswith('@teknoparkistanbul.com.tr'):
            raise ValidationError({
                'email': _('Teknopark rolü için sadece @teknoparkistanbul.com.tr uzantılı e-posta adresi kullanılabilir.')
            })

        # Yatırımcı rolü için yatırım miktarı zorunlu
        if self.role == 'investor' and not self.yatirim_miktari:
            raise ValidationError({
                'yatirim_miktari': _('Yatırımcı olarak yatırım yapmayı düşündüğün miktarı belirtmelisin.')
            })

        # Girişimci rolü için talep edilen yatırım miktarı zorunlu
        if self.role == 'entrepreneur' and not self.talep_edilen_yatirim:
            raise ValidationError({
                'talep_edilen_yatirim': _('Girişimci olarak talep ettiğin yatırım miktarını belirtmelisin.')
            })

class PersonalNote(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.user.first_name})"

class MeetingTable(models.Model):
    meeting_day = models.ForeignKey('MeetingDay', on_delete=models.CASCADE, related_name='tables')
    table_number = models.PositiveIntegerField()
    investor = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'investor'})

    def __str__(self):
        return f"{self.meeting_day.date} - Masa {self.table_number}"

# Toplantı Günü
class MeetingDay(models.Model):
    date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    total_tables = models.IntegerField(null=True, blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'is_staff': True}, null=True, blank=True)

    def __str__(self):
        return str(self.date) if self.date else "Tarih belirtilmedi"
# Eşleştirme (randevu)
class MatchProposal(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="sent_proposals")
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="received_proposals")
    meeting_day = models.ForeignKey(MeetingDay, on_delete=models.CASCADE)
    table_number = models.IntegerField()
    start_datetime = models.DateTimeField()
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Beklemede'),
        ('accepted', 'Kabul Edildi'),
        ('rejected', 'Reddedildi'),
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def is_active(self):
        return self.status == 'pending'


class Match(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )

    entrepreneur = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="entrepreneur_matches")
    investor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="investor_matches")
    meeting_day = models.ForeignKey(MeetingDay, on_delete=models.CASCADE)
    table_number = models.IntegerField()
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    entrepreneur_arrived = models.BooleanField(default=False)
    investor_arrived = models.BooleanField(default=False)
    meeting_ended = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='accepted')  # 'accepted' varsayalım
    entrepreneur_accepted = models.BooleanField(default=False)
    investor_accepted = models.BooleanField(default=False)

    def meeting_started(self):
        return self.entrepreneur_arrived and self.investor_arrived and not self.meeting_ended

    def meeting_expired(self):
        if not self.meeting_started():
            return False
        end_time = self.start_datetime + timedelta(minutes=5)
        return timezone.now() >= end_time

    def reject_proposal(self):
        """Teklifi reddetmek için status 'rejected' olarak ayarlanır."""
        if self.status != 'rejected':
            self.status = 'rejected'
            self.save()
            raise ValidationError("Teklif reddedildi!")

    def accept_proposal(self):
        """Teklifi kabul etmek için status 'accepted' olarak ayarlanır."""
        if self.status == 'pending':
            self.status = 'accepted'
            self.save()

    def __str__(self):
        return f"Toplantı"


class Evaluation(models.Model):
    ROLE_CHOICES = (
        ('entrepreneur', 'Girişimci'),
        ('investor', 'Yatırımcı'),
    )

    match = models.ForeignKey('Match', on_delete=models.CASCADE)
    evaluator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    # Ortak alan
    overall_satisfaction = models.IntegerField()  # 1 - 5 arası

    # Girişimci özel alanlar
    investor_interest = models.IntegerField(null=True, blank=True)
    constructive_feedback = models.IntegerField(null=True, blank=True)
    expression_opportunity = models.IntegerField(null=True, blank=True)
    meeting_environment = models.IntegerField(null=True, blank=True)

    # Yatırımcı özel alanlar
    presentation_effectiveness = models.IntegerField(null=True, blank=True)
    idea_potential = models.IntegerField(null=True, blank=True)
    time_efficiency = models.IntegerField(null=True, blank=True)
    communication_skills = models.IntegerField(null=True, blank=True)

    submitted_at = models.DateTimeField(auto_now_add=True)
