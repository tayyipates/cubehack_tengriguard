from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Match, MeetingDay, Category, Evaluation, MeetingTable

admin.site.register(Category)

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name', 'uygunluk', 'role', 'is_staff', 'is_active','ths')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('email',)
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Kişisel Bilgiler', {'fields': ('first_name', 'last_name', 'uygunluk', 'role', 'categories')}),
        ('Şirket Bilgileri', {'fields': ('sirket', 'sirket_bilgileri', 'web_adresi', 'iletisim_emaili', 'sirket_logosu', 'yatirim_miktari', 'talep_edilen_yatirim', 'ths')}),
        ('İzinler', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role', 'is_staff', 'is_active')}
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)


class MeetingTableInline(admin.TabularInline):
    model = MeetingTable
    extra = 0

@admin.register(MeetingDay)
class MeetingDayAdmin(admin.ModelAdmin):
    inlines = [MeetingTableInline]


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = (
        'entrepreneur', 'investor', 'meeting_day',
        'table_number', 'start_datetime', 'end_datetime',
        'entrepreneur_arrived', 'investor_arrived'
    )
    list_filter = ('meeting_day', 'table_number')
    ordering = ('start_datetime',)

admin.site.register(Evaluation)