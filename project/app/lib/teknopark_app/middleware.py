from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q
from .models import Match  # Match modelini burada alabilirsin çünkü circular yok artık 😇


class EvaluationRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Kullanıcı giriş yapmamışsa veya admin panelindeyse middleware'i pas geç
        if not request.user.is_authenticated or request.path.startswith('/admin/'):
            return self.get_response(request)

        # Bazı sayfalar bu kontrolün dışında tutulmalı (örneğin değerlendirme formu ve logout)
        allowed_paths = [
            reverse('logout'),
        ]

        # Dynamic reverse URL'leri şablona çevir
        try:
            allowed_paths += [
                reverse('degerlendirme_formu', kwargs={'match_id': 1}).rsplit('1', 1)[0],
                reverse('toplanti_bitir', kwargs={'match_id': 1}).rsplit('1', 1)[0],
            ]
        except:
            pass  # URL'ler yüklenmemiş olabilir, safe fallback

        # İzinli yollardan birindeyse kontrolü atla
        if any(request.path.startswith(path) for path in allowed_paths):
            return self.get_response(request)

        # Kullanıcının bitmiş ama değerlendirmediği toplantıları kontrol et
        pending_matches = Match.objects.filter(
            meeting_ended=True
        ).filter(
            Q(entrepreneur=request.user) | Q(investor=request.user)
        ).exclude(
            evaluation__evaluator=request.user  # ❗️Dikkat: `related_name='evaluation'` ise bu şekilde!
        )

        if pending_matches.exists():
            first_pending = pending_matches.first()
            messages.warning(request, "Bitmiş bir toplantıyı değerlendirmeden devam edemezsin 💬")
            return redirect('degerlendirme_formu', match_id=first_pending.id)

        return self.get_response(request)
