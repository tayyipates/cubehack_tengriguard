# app/urls.py

from django.urls import path
from . import views
from .views import CustomLoginView
from django.contrib.auth.views import LogoutView
from .views import EvaluationListView, EvaluationDetailView

urlpatterns = [
    path('edit-meeting-day/<int:meeting_day_id>/', views.edit_meeting_day, name='edit_meeting_day'),
    path('delete-entrepreneur/<int:user_id>/', views.delete_entrepreneur, name='delete_entrepreneur'),
    path('delete-investor/<int:user_id>/', views.delete_investor, name='delete_investor'),
    path('formlar/', EvaluationListView.as_view(), name='evaluation_list'),
    path('formlar/<int:pk>/', EvaluationDetailView.as_view(), name='evaluation_detail'),
    path('', views.home_view, name='home'),
    path('add_tables/', views.add_tables, name='add_tables'),
    path('eslesmelerim/', views.eslesmlerim, name='eslesmlerim'),
    path('accept-match/<int:match_id>/', views.accepted_match, name='accepted_match'),
    path('reject-match/<int:match_id>/', views.rejected_match, name='rejected_match'),
    path('teknopark/saat/', views.manage_meeting_days, name='manage_meeting_days'),
    path('degerlendirme/<int:match_id>/', views.degerlendirme_formu, name='degerlendirme_formu'),
    path('notlarim/', views.notes_list_view, name='notes_list'),
    path('notlarim/yeni/', views.create_note_view, name='create_note'),
    path('notes/edit/<int:note_id>/', views.edit_note_view, name='edit_note'),
    path('accept-match/', views.accept_match, name='accept_match'),
    path('toplanti-bitir/<int:match_id>/', views.toplanti_bitir_view, name='toplanti_bitir'),
    path('start-match/', views.start_match_view, name='start_match'),
    path('match/<int:match_id>/arrived/', views.masaya_geldim_view, name='masaya_geldim'),
    path('register/', views.register_view, name='register'),
    path('login/', views.custom_login_view, name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('match/<int:match_id>/arrived/', views.run_matching_view, name='run_matching_view'),
    path('liste/girisimciler/', views.girisimci_listesi, name='girisimci_listesi'),
    path('liste/yatirimcilar/', views.yatirimci_listesi, name='yatirimci_listesi'),
]
