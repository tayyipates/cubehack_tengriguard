# 🌉 Teknopark İstanbul Yatırımcı-Girişimci Eşleştirme Uygulaması

Bu mobil uygulama, Teknopark İstanbul tarafından düzenlenen yatırımcı-girişimci eşleştirme etkinliklerinde kullanılmak üzere geliştirilmiştir. Etkinlik boyunca yatırımcı ve girişimcilerin kategorilere göre eşleşmelerini sağlamak, toplantı süreçlerini yönetmek ve değerlendirme formlarını toplamak amacıyla kullanılır.

---

## 🧪 Kullanılan Teknolojiler

- **Mobil Geliştirme:**
  - Android: Flutter
  - iOS: Swift (apk yapılamadı)
- **Bildirim Servisi:** Firebase FCM (Yapılamadı)

## 👥 Takım Üyeleri ve Rolleri

| İsim         | Rol                                      |
|--------------|-------------------------------------------|
| Tayyip Ateş  | Proje Yöneticisi, Sunum ve Tanıtım Videoları |
| Fatih Bozkurt| Tüm mobil uygulama geliştirme ve teknik işlemler |

## ⚙️ Kurulum Talimatları

> **Not:** Uygulama sadece Teknopark İstanbul’un etkinliği için geliştirilmiştir. Kurulum ve kullanım hakları Teknopark yetkililerine aittir.

### Android
1. `apk` dosyasını Android cihazınıza yükleyin.
2. Gerekli izinleri vererek uygulamayı başlatın.

### iOS
1. Uygulama, TestFlight veya doğrudan kurulumla sağlanacaktır.
2. Geliştirici onaylı cihazlarda çalışacaktır.

### Kullanıcı Rolleri
- **Teknopark Yetkilisi**
  - Admin panelinden masa atama, saat tanımlama ve kullanıcı yönetimi yapabilir.
  - Yalnızca `@teknoparkistanbul.com.tr` uzantılı adreslerle kayıt olunabilir.
  - Form değerlendirme ekranından görüşmelerin sonuçlarını izleyebilir.
  - Yatırımcı ve girişimci listelerine ulaşabilir gerek gördüğü kullanıcıları silebilir.

### 💼 Yatırımcılar

- Kategorilere göre girişimcilerle eşleşir.
- Toplantılara katılır.
- Değerlendirme formu doldurur.
- “Toplantıya geldim” ve “Toplantıyı bitirdim” işlemlerini gerçekleştirir.
- Toplantı sonrası ikinci görüşmeleri sistem üzerinden değil, bireysel olarak planlar. Uygulama bu görüşmeleri yönetmez. Taraflar iletişim bilgilerini kullanarak irtibata geçer.

### 🚀 Girişimciler

- Kategorilere göre yatırımcılarla eşleşir.
- Toplantılara katılır.
- Tanıtım yapar, değerlendirme formu doldurur.
- “Toplantıya geldim” ve “Toplantıyı bitirdim” işlemlerini gerçekleştirir.
- Toplantı sonrası ikinci görüşmeleri bireysel olarak planlar.

# 🧩 Başlıca Özellikler

- 🔐 Kayıt ve giriş sistemi (e-posta doğrulamalı, KVKK onayı) (KVKK metni Teknopark yetkilileri tarafından alınarak uygulamaya eklenecektir.)
- 🗂️ Çoklu kategori seçimi (**39 sabit kategori – aşağıda listelenmiştir**)
- 🧠 Kategori bazlı eşleşme algoritması
- ⏰ Teknopark yetkilisi tarafından tanımlanan saat aralıklarında otomatik toplantı saati belirleme
- 🪑 Masa atama (aynı masaya birden fazla kişi atanamaz)
- 📲 Bildirim sistemi (5 dakika önce toplantı bildirimi)
- ✅ Karşılıklı onay mekanizmasıyla eşleşme
- 📅 Sadece toplantı günü eşleşme yapılabilir
- 📥 Toplantı sonrası değerlendirme formu (manuel tıklama veya 5 dk içinde otomatik gösterim)
- 📝 Not alma alanı
- 📤 Görüşme formlarının kullanıcı bazlı listelenmesi
- ❌ Dışa aktarım yapılmaz (formlar uygulama dışına çıkartılamaz)

### Toplantı Düzenleme
- Teknopark yetkilisi toplantı günün ve toplantıların yapılacağı saat aralığını belirler.
- Masa atamaları teknopark yetkilisi tarafından yapılır
  - Masa atamaları kısmında kaç adet masa olacağı bilgisi ve masalara hangi yatırımcı şirketlerin yerleşeceğini teknopark yetkilisi belirler.
    - Örn. Masa-1 A şirketi, Masa-2 B şirketi
    - Toplantı dönemi boyunca yatırımcı şirketler sabit masada kalır girişimciler görüşmeleri yapmak için uygulamadan eşleştikleri şirketleri ve bulundukları masaları takip edebilir.
    
### Toplantı Akışı
1. Her iki taraf eşleşmeyi onaylar.
2. Sistem otomatik olarak saat ve masa ataması yapar.
3. 5 dakika önce bildirim gönderilir.
4. Toplantıya katılım butonları ile süreç başlar. Katılımcıdan biri zamanında gelmezse toplantı ileri saatlere ertelenir.
5. Toplantı süresi: 5 dk  
   Masayı boşaltma süresi: 5 dk
6. Toplantı sonrası değerlendirme formu açılır (manuel veya otomatik).
7. Tüm formlar sistemde saklanır, değiştirilemez, dışa aktarılamaz.

### Değerlendirme Formu
- Değerlendirme formu soruları Teknopark İstanbul tarafından sağlanacak yönergeye göre dinamik olarak güncellenebilir.
- Örnek yapı:
  - 1–5 arası puanlanabilir sorular
  - “İkinci bir görüşme talep ediyor musunuz?” (Evet/Hayır)
    - (*Cevabınız evet ise yatırımcı/girişimci şirketin iletişim bilgilerini almayı unutmayınız*)

### Diğer Notlar
- Uygulama sadece mobil platformlar için geliştirilmiştir.
- Masa atamaları ve toplantı saatleri sistem tarafından otomatik olarak yapılır.
- Tüm eşleşmeler sadece toplantı gününde yapılabilir.
- Girişimci ve yatırımcılar kendilerine özel not alanında istedikleri gibi notlar alabilir toplantı sırasında aldıkları notların takibini daha sonra yapabilir. Notlar kısmı kullanıcıa özeldir yetkililer dahil kullanıcı hariç kimse notlar kısmındaki belgeleri göremez.
> Giriş yapmadan kullanılabilecek herhangi bir modül bulunmamaktadır. Sistemde ilerleyebilmek için e-posta ve şifre ile kayıt olunması gerekir.

## 📚 Kategoriler (39 Adet)

1. Robotik ve Otomasyon Sistemleri  
2. Havacılık ve İHA Sistemleri  
3. Uzay ve Uydu Teknolojileri  
4. Denizcilik ve Sualtı Sistemleri  
5. Sağlık ve Medikal Teknolojiler  
6. Enerji ve Yenilenebilir Enerji Sistemleri  
7. İleri Elektronik Teknolojileri  
8. İleri Mühendislik ve Mekatronik Sistemler  
9. İleri Malzeme ve Nanoteknoloji  
10. Savunma ve Güvenlik Sistemleri  
11. Haberleşme ve Telekomünikasyon Sistemleri  
12. Yapay Zeka ve Makine Öğrenimi Uygulamaları  
13. Bilişim ve Yazılım Teknolojileri  
14. Siber Güvenlik ve Kriptografi Sistemleri  
15. Endüstri 4.0 ve Akıllı Üretim Sistemleri  
16. İnşaat Teknolojileri ve Akıllı Altyapılar  
17. Otomotiv ve Elektrikli Araç Teknolojileri  
18. Tarım ve Tarım Teknolojileri  
19. Afet Yönetimi ve Arama Kurtarma Teknolojileri  
20. Sürdürülebilirlik ve Çevre Teknolojileri  
21. Biyoteknoloji ve Genetik Mühendisliği  
22. Konumlandırma ve Navigasyon Sistemleri  
23. Test, Ölçüm ve Kalibrasyon Sistemleri  
24. Eğitim ve Teknolojik Simülasyon Sistemleri  
25. Akıllı Malzemeler ve Fonksiyonel Ürünler  
26. Veri Bilimi ve Büyük Veri Sistemleri  
27. Finansal Teknolojiler (FinTech)  
28. Oyun ve Simülasyon Teknolojileri  
29. Yangın Algılama, Söndürme ve Acil Müdahale Sistemleri  
30. Genetik, Sentetik Biyoloji ve Biyoteknoloji  
31. Gıda Teknolojileri ve Tarımsal Biyoteknoloji  
32. Kimya ve Endüstriyel Kimyasal Üretim Teknolojileri  
33. Batarya, Yakıt Hücresi ve Enerji Depolama Sistemleri  
34. Akıllı Tarım ve Tarım Otomasyonu  
35. Tekstil ve Giyilebilir Teknolojiler  
36. Nöroteknoloji ve Beyin-Bilgisayar Arayüzleri (BCI)  
37. Artırılmış Gerçeklik (AR), Sanal Gerçeklik (VR) ve Karma Gerçeklik (XR)  
38. Hukuk Teknolojileri (LegalTech)  
39. Lojistik ve Depolama Otomasyonu