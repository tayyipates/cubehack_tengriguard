from django import forms
from .models import CustomUser, Category, Evaluation
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm





class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['overall_satisfaction']

    def __init__(self, *args, **kwargs):
        role = kwargs.pop('role', None)
        super().__init__(*args, **kwargs)

        self.fields['overall_satisfaction'].label = "Genel Memnuniyet"
        self.fields['overall_satisfaction'] = forms.ChoiceField(
            label="Genel Memnuniyet",
            choices=[(i, str(i)) for i in range(1, 6)],
            widget=forms.RadioSelect
        )

        if role == 'entrepreneur':
            self.fields['investor_interest'] = forms.ChoiceField(
                label="Yatırımcının ilgisi yeterli miydi?",
                choices=[(i, str(i)) for i in range(1, 6)],
                widget=forms.RadioSelect
            )
            self.fields['constructive_feedback'] = forms.ChoiceField(
                label="Geri bildirimleri yapıcı mıydı?",
                choices=[(i, str(i)) for i in range(1, 6)],
                widget=forms.RadioSelect
            )
            self.fields['expression_opportunity'] = forms.ChoiceField(
                label="Kendinizi ifade etme fırsatı buldunuz mu?",
                choices=[(i, str(i)) for i in range(1, 6)],
                widget=forms.RadioSelect
            )
            self.fields['meeting_environment'] = forms.ChoiceField(
                label="Toplantı ortamı nasıldı?",
                choices=[(i, str(i)) for i in range(1, 6)],
                widget=forms.RadioSelect
            )

        elif role == 'investor':
            self.fields['presentation_effectiveness'] = forms.ChoiceField(
                label="Girişimcinin sunumu ne kadar etkileyiciydi?",
                choices=[(i, str(i)) for i in range(1, 6)],
                widget=forms.RadioSelect
            )
            self.fields['idea_potential'] = forms.ChoiceField(
                label="İş fikrinin potansiyeli hakkında ne düşünüyorsunuz?",
                choices=[(i, str(i)) for i in range(1, 6)],
                widget=forms.RadioSelect
            )
            self.fields['time_efficiency'] = forms.ChoiceField(
                label="Toplantı süresi yeterli miydi?",
                choices=[(i, str(i)) for i in range(1, 6)],
                widget=forms.RadioSelect
            )
            self.fields['communication_skills'] = forms.ChoiceField(
                label="İletişim yetkinliğini nasıl değerlendirirsiniz?",
                choices=[(i, str(i)) for i in range(1, 6)],
                widget=forms.RadioSelect
            )

class UserProfileForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'uygunluk', 'categories','sirket','sirket_bilgileri','web_adresi','iletisim_emaili','sirket_logosu']
class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = (
        ('investor', 'Yatırımcı'),
        ('entrepreneur', 'Girişimci'),
        ('teknopark', 'Teknopark Yetkilisi'),
    )

    THS_CHOICES = [(str(i), f"THS-{i} seviyesi") for i in range(1, 10)]

    role = forms.ChoiceField(choices=ROLE_CHOICES, label='Rolünü seç')
    ths = forms.ChoiceField(
        choices=THS_CHOICES,
        required=False,
        label="Teknoloji Hazırlık Seviyesi (THS)"
    )

    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'email', 'password1', 'password2',
            'categories', 'sirket', 'sirket_bilgileri', 'web_adresi',
            'iletisim_emaili', 'sirket_logosu', 'role',
            'yatirim_miktari', 'talep_edilen_yatirim', 'ths'
        ]

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        yatirim_miktari = cleaned_data.get('yatirim_miktari')
        talep_edilen_yatirim = cleaned_data.get('talep_edilen_yatirim')
        ths = cleaned_data.get('ths')

        if role == 'teknopark':
            cleaned_data['sirket'] = ''
            cleaned_data['sirket_bilgileri'] = ''
            cleaned_data['web_adresi'] = None
            cleaned_data['iletisim_emaili'] = None
            cleaned_data['sirket_logosu'] = None
            cleaned_data['yatirim_miktari'] = None
            cleaned_data['talep_edilen_yatirim'] = None
            cleaned_data['ths'] = None

        elif role == 'investor':
            if not yatirim_miktari:
                self.add_error('yatirim_miktari', 'Yatırımcılar için yatırım miktarı zorunludur.')
            cleaned_data['talep_edilen_yatirim'] = None
            cleaned_data['ths'] = None

        elif role == 'entrepreneur':
            if not talep_edilen_yatirim:
                self.add_error('talep_edilen_yatirim', 'Girişimciler için talep edilen yatırım zorunludur.')
            if not ths:
                self.add_error('ths', 'THS seviyesi seçilmelidir.')
            cleaned_data['yatirim_miktari'] = None

        return cleaned_data

from django.contrib.auth import authenticate

class CustomLoginForm(forms.Form):
    email = forms.EmailField(label="E-posta", widget=forms.EmailInput(attrs={'autofocus': True}))
    password = forms.CharField(label="Şifre", strip=False, widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user = authenticate(email=email, password=password)
            if self.user is None:
                raise forms.ValidationError("Geçersiz e-posta ya da şifre")
        return self.cleaned_data

    def get_user(self):
        return self.user
    email = forms.CharField(
        label='Email',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email adresini yaz'})
    )
    password = forms.CharField(
        label='Şifre',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Şifren buraya :)'})
    )