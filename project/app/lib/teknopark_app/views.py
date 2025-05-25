from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import CustomUser, MeetingDay, Match, PersonalNote, Evaluation,MatchProposal, MeetingTable
from datetime import datetime, timedelta, time
from django.db.models import Q
from django.shortcuts import get_object_or_404
import random
from django.contrib import messages
from django.utils import timezone

@login_required
def toplanti_bitir_view(request, match_id):
    match = get_object_or_404(Match, id=match_id)

    if request.user not in [match.entrepreneur, match.investor]:
        return HttpResponseForbidden("Bu toplantıya erişimin yok ")

    if not match.meeting_ended:
        match.meeting_ended = True
        match.save()
        messages.success(request, "Toplantıyı başarıyla bitirdin ")

    # Kullanıcının bu toplantı için değerlendirme yapıp yapmadığını kontrol edelim
    evaluation_exists = Evaluation.objects.filter(match=match, evaluator=request.user).exists()

    if not evaluation_exists:
        messages.info(request, "Bu toplantı için değerlendirme yapmalısın ")
        return redirect('degerlendirme_formu', match_id=match.id)

    # Eğer zaten değerlendirme yapmışsa dashboard'a yönlendir
    return redirect('dashboard')

@login_required
def notes_list_view(request):
    notes = PersonalNote.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notes/notes_list.html', {'notes': notes})

@login_required
def create_note_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        if not title or not content:
            messages.error(request, "Başlık ve not içeriği zorunludur! 😮")
            return redirect('create_note')

        PersonalNote.objects.create(user=request.user, title=title, content=content)
        messages.success(request, "Notun kaydedildi! 🥳")
        return redirect('notes_list')

    return render(request, 'notes/create_note.html')




@login_required
def edit_note_view(request, note_id):
    note = get_object_or_404(PersonalNote, id=note_id, user=request.user)

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        if not title or not content:
            messages.error(request, "Başlık ve içerik boş bırakılamaz! 😵")
            return redirect('edit_note', note_id=note.id)

        note.title = title
        note.content = content
        note.save()

        messages.success(request, "Not başarıyla güncellendi! ✨")
        return redirect('notes_list')

    return render(request, 'notes/edit_note.html', {'note': note})










from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from datetime import datetime, timedelta
from .models import CustomUser, MeetingDay, Match

@login_required
def start_match_view(request):
    user = request.user
    role_opposite = 'investor' if user.role == 'entrepreneur' else 'entrepreneur'
    user_categories = user.categories.all()
    
    # Kategori bilgileri
    category_count = user_categories.count()
    category_names = [c.name for c in user_categories]
    
    try:
        meeting_day = MeetingDay.objects.latest('date')
    except MeetingDay.DoesNotExist:
        return render(request, 'start_match.html', {
            'error': "Henüz bir toplantı günü ayarlanmadı, lütfen Teknopark yetkilileriyle iletişime geçin 💬"
        })

    all_opposite_users = CustomUser.objects.filter(role=role_opposite).exclude(id=user.id)
    available_users = all_opposite_users.filter(uygunluk=True)

    # Kategori filtresi
    candidates = available_users.filter(categories__in=user_categories).distinct() if user_categories.exists() else available_users
    
    # Tüm eşleşmeleri çek
    existing_matches = Match.objects.filter(meeting_day=meeting_day)

    # Dolu olan masa ve saatleri datetime olarak kaydet
    used_slots = set((m.table_number, m.start_datetime) for m in existing_matches)

    available_slots = []
    current_time = datetime.combine(meeting_day.date, meeting_day.start_time)
    end_time = datetime.combine(meeting_day.date, meeting_day.end_time)

    while current_time + timedelta(minutes=5) <= end_time:
        for table in range(1, meeting_day.total_tables + 1):
            is_full = (table, current_time) in used_slots
            available_slots.append({
                'time': current_time.strftime('%H:%M'),
                'table': table,
                'datetime': current_time.isoformat(),  # ISO format - post data için güvenli
                'is_full': is_full
            })
        current_time += timedelta(minutes=10)

    debug_info = {
        'user_role': user.role,
        'opposite_role': role_opposite,
        'user_category_count': category_count,
        'user_categories': category_names,
        'all_opposite_count': all_opposite_users.count(),
        'available_users_count': available_users.count(),
        'candidates_with_category_count': candidates.count(),
    }

    return render(request, 'start_match.html', {
        'candidates': candidates,
        'available_slots': available_slots,
        'meeting_day': meeting_day,
        'debug_info': debug_info,
    })




@login_required
def accept_match(request):
    if request.method == 'POST':
        matched_user_id = request.POST.get('matched_user_id')
        selected_slot = request.POST.get('selected_slot')

        if not matched_user_id or not selected_slot:
            return render(request, 'start_match.html', {'error': 'Eksik bilgi!'})

        matched_user = get_object_or_404(CustomUser, id=matched_user_id)

        try:
            datetime_str, table_number_str = selected_slot.split('|')
            selected_datetime = datetime.fromisoformat(datetime_str)
            table_number = int(table_number_str)
        except Exception as e:
            return render(request, 'start_match.html', {'error': 'Zaman veya masa hatalı!'})

        try:
            meeting_day = MeetingDay.objects.latest('date')
        except MeetingDay.DoesNotExist:
            return render(request, 'start_match.html', {'error': 'Toplantı günü bulunamadı!'})

        e_user = request.user if request.user.role == "entrepreneur" else matched_user
        i_user = request.user if request.user.role == "investor" else matched_user

        clean_selected_time = selected_datetime.replace(second=0, microsecond=0)

        # Eşleşme arama
        match = Match.objects.filter(
            meeting_day=meeting_day,
            table_number=table_number,
            start_datetime=clean_selected_time,
            entrepreneur=e_user,
            investor=i_user
        ).first()

        if match:
            # Eğer eşleşme varsa, sadece status'ü güncelle
            if request.user.role == "entrepreneur":
                match.status = 'accepted'  # Eşleşme kabul edilmiştir
                match.entrepreneur_accepted = True  # Girişimci geldi
            else:
                match.status = 'accepted'  # Eşleşme kabul edilmiştir
                match.investor_accepted = True  # Yatırımcı geldi
            match.save()
        else:
            # Yeni eşleşme oluşturuluyor
            match = Match.objects.create(
                entrepreneur=e_user,
                investor=i_user,
                meeting_day=meeting_day,
                table_number=table_number,
                start_datetime=clean_selected_time,
                end_datetime=clean_selected_time + timedelta(minutes=5),
                status='pending'
            )
            # Eğer yatırımcı teklif gönderdiyse
            if request.user.role == "investor":
                match.investor_accepted = True  # Yatırımcı geldi
            else:
                match.entrepreneur_accepted= True  # Girişimci geldi
            match.save()

        return redirect('dashboard')

    return redirect('start_match')




@login_required
def accepted_match(request, match_id):
    match = get_object_or_404(Match, id=match_id)

    # Eşleşmeyi kabul etme
    if request.user == match.entrepreneur:
        match.entrepreneur_accepted = True
        match.status = 'accepted'  # Eşleşme kabul edildi olarak işaretlensin
    elif request.user == match.investor:
        match.investor_accepted = True
        match.status = 'accepted'  # Eşleşme kabul edildi olarak işaretlensin

    match.save()
    return redirect('dashboard')


@login_required
def rejected_match(request, match_id):
    match = get_object_or_404(Match, id=match_id)

    # Eşleşmeyi reddetme
    if request.user == match.entrepreneur:
        match.status = 'rejected'
    elif request.user == match.investor:
        match.status = 'rejected'

    match.save()
    return redirect('dashboard')



# Kullanıcı rol kontrolü
def is_admin(user):
    return user.is_superuser

# Ana sayfa
def home_view(request):
    return render(request, 'home.html')

# Kayıt
from .forms import CustomLoginForm, CustomUserCreationForm, UserProfileForm
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)  # request.FILES'ı ekledik
        if form.is_valid():
            user = form.save(commit=False)  # henüz kaydetmiyoruz, önce kontrol yapacağız

            # Teknopark rolü + geçerli e-posta kontrolü
            if user.role == 'teknopark' and user.email.endswith('@teknoparkistanbul.com.tr'):
                user.is_staff = True
                user.is_superuser = True
            else:
                if user.role == 'teknopark':
                    form.add_error('email', 'Teknopark rolü için yalnızca @teknoparkistanbul.com.tr uzantılı e-posta adresi kullanılabilir.')
                    return render(request, 'register.html', {'form': form})

            user.save()  # kontroller tamam, artık kaydedebiliriz
            login(request, user)  # Giriş yapalım 
            return redirect('dashboard')  
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})




# Giriş
from django.contrib.auth.views import LoginView
class CustomLoginView(LoginView):
    authentication_form = CustomLoginForm
    template_name = 'login.html'

# Çıkış
def logout_view(request):
    logout(request)
    return redirect('login')


from datetime import date
from .models import Evaluation  # Evaluation modelin varsa bu satır olsun

@login_required
def degerlendirme_formu(request, match_id):
    match = get_object_or_404(Match, id=match_id)

    # Kullanıcının rolünü belirle
    if request.user == match.entrepreneur:
        role = "entrepreneur"
    elif request.user == match.investor:
        role = "investor"
    else:
        return HttpResponseForbidden("Bu toplantıya ait değilsiniz.")

    # Daha önce değerlendirme yapıldı mı kontrolü
    if Evaluation.objects.filter(match=match, evaluator=request.user).exists():
        messages.info(request, "Zaten değerlendirme yaptınız.")
        return redirect('dashboard')

    if request.method == 'POST':
        # Ortak alanlar
        overall_satisfaction = request.POST.get('overall_satisfaction')
        time_efficiency = request.POST.get('time_efficiency')

        evaluation_data = {
            'match': match,
            'evaluator': request.user,
            'role': role,
            'overall_satisfaction': overall_satisfaction,
            'time_efficiency': time_efficiency,
            'submitted_at': timezone.now(),
        }

        # Role'e göre ek alanlar
        if role == "investor":
            evaluation_data.update({
                'idea_potential': request.POST.get('idea_potential'),
                'presentation_effectiveness': request.POST.get('presentation_effectiveness'),
            })
        elif role == "entrepreneur":
            evaluation_data.update({
                'expression_opportunity': request.POST.get('expression_opportunity'),
                'constructive_feedback': request.POST.get('constructive_feedback'),
                'investor_interest': request.POST.get('investor_interest'),
            })

        # Kaydet
        Evaluation.objects.create(**evaluation_data)
        messages.success(request, "Değerlendirme başarıyla kaydedildi.")
        return redirect('dashboard')

    return render(request, 'degerlendirme_formu.html', {
        'match': match,
        'role': role
    })


from django.utils import timezone
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.db.models import Q

def is_teknopark_user(user):
    return user.is_staff

def girisimci_listesi(request):
    girisimciler = CustomUser.objects.filter(role='entrepreneur')
    return render(request, 'kullanicilar/girisimciler.html', {'kullanicilar': girisimciler})

def delete_entrepreneur(request, user_id):
    user_to_delete = get_object_or_404(CustomUser, id=user_id)
    user_to_delete.delete()
    return redirect('girisimci_listesi')

def delete_investor(request, user_id):
    user_to_delete = get_object_or_404(CustomUser, id=user_id)
    user_to_delete.delete()
    return redirect('yatirimci_listesi')

def yatirimci_listesi(request):
    yatirimcilar = CustomUser.objects.filter(role='investor')
    return render(request, 'kullanicilar/yatirimcilar.html', {'kullanicilar': yatirimcilar})

def custom_login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('dashboard')  # yönlendirme istediğin sayfa
    else:
        form = CustomLoginForm()

    return render(request, 'login.html', {'form': form})

class EvaluationListView(ListView):
    model = Evaluation
    template_name = 'evaluations/evaluation_list.html'
    context_object_name = 'evaluations'
    paginate_by = 20

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        qs = super().get_queryset().select_related('evaluator', 'match')

        if query:
            qs = qs.filter(
                Q(evaluator__first_name__icontains=query) |
                Q(evaluator__last_name__icontains=query) |
                Q(evaluator__email__icontains=query)
            )

        # Match'leri gruplayarak her birini, hem girişimci hem de yatırımcıyı gösterecek şekilde sıralıyoruz.
        return qs.order_by('match__id', '-submitted_at')



@method_decorator(user_passes_test(is_teknopark_user), name='dispatch')
class EvaluationDetailView(DetailView):
    model = Evaluation
    template_name = 'evaluations/evaluation_detail.html'
    context_object_name = 'evaluation'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        evaluation = self.get_object()

        # Girişimci ve Yatırımcıyı context'e ekliyoruz
        context['entrepreneur_evaluation'] = Evaluation.objects.filter(match=evaluation.match, role='entrepreneur').first()
        context['investor_evaluation'] = Evaluation.objects.filter(match=evaluation.match, role='investor').first()

        return context


@login_required
def dashboard_view(request):
    user = request.user

    # Kullanıcının tüm eşleşmeleri
    matches = Match.objects.filter(
        Q(entrepreneur=user) | Q(investor=user)
    ).order_by('start_datetime')

    match_data = []
    for match in matches:
        if user == match.entrepreneur:
            other_user = match.investor
            user_arrived = match.entrepreneur_arrived
        else:
            other_user = match.entrepreneur
            user_arrived = match.investor_arrived

        # Saat 09:00'dan 5 dakika önce gelen uyarı
        time_left = match.start_datetime - timezone.now()
        five_minutes_left = timedelta(minutes=5)

        if time_left <= five_minutes_left:
            message = "Lütfen masanıza geçin ve masaya geldim butonuna tıklayın."
        elif not user_arrived and time_left <= timedelta(minutes=0):
            message = "Toplantınız ileri bir dakikaya ertelenmiştir. Lütfen bulunduğunuz masayı boşaltınız."
        else:
            message = ""

        evaluation_exists = Evaluation.objects.filter(match=match, evaluator=user).exists()

        match_data.append({
            'match': match,
            'other_user': other_user,
            'user_arrived': user_arrived,
            'meeting_started': match.meeting_started(),
            'evaluation_exists': evaluation_exists,
            'message': message,
            'status': match.status
        })

    return render(request, 'dashboard.html', {
        'match_data': match_data,
        'today': date.today(),
    })

@login_required
def eslesmlerim(request):
    user = request.user

    # Kullanıcının tüm eşleşmeleri
    matches = Match.objects.filter(
        Q(entrepreneur=user) | Q(investor=user)
    ).order_by('start_datetime')

    match_data = []
    for match in matches:
        if user == match.entrepreneur:
            other_user = match.investor
            user_arrived = match.entrepreneur_arrived
        else:
            other_user = match.entrepreneur
            user_arrived = match.investor_arrived

        # Saat 09:00'dan 5 dakika önce gelen uyarı
        time_left = match.start_datetime - timezone.now()
        five_minutes_left = timedelta(minutes=5)

        if time_left <= five_minutes_left:
            message = "Lütfen masanıza geçin ve masaya geldim butonuna tıklayın."
        elif not user_arrived and time_left <= timedelta(minutes=0):
            message = "Toplantınız ileri bir dakikaya ertelenmiştir. Lütfen bulunduğunuz masayı boşaltınız."
        else:
            message = ""

        evaluation_exists = Evaluation.objects.filter(match=match, evaluator=user).exists()

        match_data.append({
            'match': match,
            'other_user': other_user,
            'user_arrived': user_arrived,
            'meeting_started': match.meeting_started(),
            'evaluation_exists': evaluation_exists,
            'message': message,
            'status': match.status
        })

    return render(request, 'eslesmelerim.html', {
        'match_data': match_data,
        'today': date.today(),
    })

from django.shortcuts import render, redirect
from .models import MeetingDay, CustomUser
from django.http import JsonResponse
import json  # json modülünü buraya ekliyoruz

@login_required
def edit_meeting_day(request, meeting_day_id):
    user = request.user
    meeting_day = get_object_or_404(MeetingDay, id=meeting_day_id)

    # Yalnızca teknopark kullanıcıları erişebilir
    if user.role != 'teknopark':
        return redirect('dashboard')

    # Yatırımcıları alıyoruz
    investors = CustomUser.objects.filter(role='investor')
    # Meeting tables'ı alıyoruz
    meeting_day_tables = meeting_day.tables.all()

    # JSON'a dönüştürmeden önce, her iki veri setini de listeye çevirelim
    investors_data = [{
        'id': investor.id,
        'first_name': investor.first_name,
        'last_name': investor.last_name,
    } for investor in investors]

    meeting_day_tables_data = [{
        'table_number': table.table_number,
        'investor_id': table.investor.id if table.investor else None,
    } for table in meeting_day_tables]

    if request.method == 'POST':
        # Verileri alıp güncelliyoruz
        meeting_day.date = request.POST.get('date')
        meeting_day.start_time = request.POST.get('start_time')
        meeting_day.end_time = request.POST.get('end_time')
        meeting_day.total_tables = int(request.POST.get('total_tables'))
        meeting_day.save()

        # Masaları güncelliyoruz
        for i in range(1, meeting_day.total_tables + 1):
            table_investor_id = request.POST.get(f'table_{i}_investor')
            investor = CustomUser.objects.get(id=table_investor_id) if table_investor_id else None
            table, created = MeetingTable.objects.get_or_create(
                meeting_day=meeting_day,
                table_number=i,
            )
            table.investor = investor
            table.save()

        return redirect('manage_meeting_days')

    return render(request, 'edit_meeting_day.html', {
        'meeting_day': meeting_day,
        'investors': json.dumps(investors_data),  # JSON formatında gönderiyoruz
        'meeting_day_tables': json.dumps(meeting_day_tables_data),  # JSON formatında gönderiyoruz
    })





@login_required
def manage_meeting_days(request):
    user = request.user

    if user.role != 'teknopark':
        return redirect('dashboard')

    meeting_days = MeetingDay.objects.all()
    investors = CustomUser.objects.filter(role='investor')

    if request.method == 'POST':
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        total_tables = int(request.POST.get('total_tables'))

        # Yeni toplantı günü ekliyoruz
        if date and start_time and end_time and total_tables:
            meeting_day = MeetingDay.objects.create(
                date=date,
                start_time=start_time,
                end_time=end_time,
                total_tables=total_tables,
                created_by=user
            )

            # Masaları ekliyoruz
            for i in range(1, total_tables + 1):
                investor_id = request.POST.get(f'table_{i}_investor')
                investor = CustomUser.objects.get(id=investor_id) if investor_id else None
                MeetingTable.objects.create(
                    meeting_day=meeting_day,
                    table_number=i,
                    investor=investor
                )

            return redirect('manage_meeting_days')  # Sayfayı yenileyip gösteriyoruz

    # Yatırımcıları JSON formatında şablona gönderiyoruz
    investors = CustomUser.objects.filter(role='investor')

    
    return render(request, 'tekno.html', {
        'meeting_days': meeting_days,
        'investors': investors,  # Yatırımcıları JSON formatında şablona gönderiyoruz
    })

from django.http import JsonResponse

@login_required
def add_tables(request):
    if request.method == 'POST':
        total_tables = int(request.POST.get('total_tables'))
        meeting_day_id = request.POST.get('meeting_day_id')
        meeting_day = MeetingDay.objects.get(id=meeting_day_id)

        # Yeni masaları ekleyelim
        for i in range(1, total_tables + 1):
            MeetingTable.objects.create(
                meeting_day=meeting_day,
                table_number=i  # Masa numarasını 1'den başlatarak artırıyoruz
            )
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)  # request.FILES'ı ekledik
        if form.is_valid():
            form.save()
            return redirect('profile')  # tekrar profile dön
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'profile.html', {'form': form})


@login_required
@require_POST
def masaya_geldim_view(request, match_id):
    match = get_object_or_404(Match, id=match_id)

    if request.user != match.entrepreneur and request.user != match.investor:
        return HttpResponseForbidden("Bu toplantıya ait değilsin aşkım 😢")

    if request.user == match.entrepreneur:
        match.entrepreneur_arrived = True
    else:
        match.investor_arrived = True

    match.save()
    return redirect('dashboard')

# Eşleştirme fonksiyonu (Admin için)
@login_required
@user_passes_test(is_admin)
def run_matching_view(request, match_id):  
    match = get_object_or_404(Match, id=match_id)
    if request.method == 'POST':
        try:
            meeting_day = MeetingDay.objects.latest('date')
        except MeetingDay.DoesNotExist:
            return render(request, 'match.html', {'error': 'Toplantı günü bulunamadı'})

        entrepreneurs = list(CustomUser.objects.filter(role='entrepreneur'))
        investors = list(CustomUser.objects.filter(role='investor'))

        current_time = datetime.combine(meeting_day.date, meeting_day.start_time)
        end_time = datetime.combine(meeting_day.date, meeting_day.end_time)
        table_count = meeting_day.total_tables

        matches = []

        while entrepreneurs and investors and current_time < end_time:
            for table in range(1, table_count + 1):
                if not entrepreneurs or not investors:
                    break

                e = entrepreneurs.pop(0)
                i = investors.pop(0)

                match = Match.objects.create(
                    entrepreneur=e,
                    investor=i,
                    meeting_day=meeting_day,
                    table_number=table,
                    start_datetime=current_time,
                    end_datetime=current_time + timedelta(minutes=5)
                )
                matches.append(match)

            current_time += timedelta(minutes=10)  # 5 dk toplantı + 5 dk boşluk

        return render(request, 'match.html', {
            'matches': matches,
            'success': True
        })

    return render(request, 'match.html')
