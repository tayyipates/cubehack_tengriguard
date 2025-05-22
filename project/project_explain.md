# Project Structure and Development Guidelines

## English

### Project Overview

This folder (`project/`) is where you'll organize your application source code for the "Çözüm Sende" Hackathon. Following a well-structured project organization will help judges evaluate your work more effectively and demonstrate your technical proficiency.

### Expected Structure

Your project should be organized according to the following structure:

```
📁 app/               (All source code of your application)
 ┣ 📁 lib/            (Main application code)
 ┣ 📁 assets/         (Images, fonts, and other static assets)
 ┣ 📁 test/           (Unit and integration tests)
 ┗ 📄 pubspec.yaml    (For Flutter) or equivalent configuration file
```

### Technical Requirements

1. **Code Organization**
   - Follow standard architectural patterns (MVC, MVVM, Clean Architecture, etc.)
   - Maintain separation of concerns
   - Use proper naming conventions
   - Include appropriate comments

2. **Source Control**
   - Make regular, meaningful commits
   - Use descriptive branch names if applicable
   - Ensure all team members contribute to the repository

3. **Quality Assurance**
   - Include basic error handling
   - Implement responsive design for different screen sizes
   - Optimize app performance where possible
   - Add unit tests for critical functionality (if time permits)

4. **Documentation**
   - Include inline code comments explaining complex logic
   - Document your architecture choices
   - Provide setup instructions in your README

### Technology Stack

Choose one of these approved mobile development stacks:

* **Cross-Platform:** Flutter
* **iOS (Native):** Swift
* **Android (Native):** Kotlin

You may use any of the recommended backend services:
* Firebase
* Supabase
* Appwrite

### Best Practices

1. **Mobile Development**
   - Follow platform-specific design guidelines
   - Ensure responsive layouts for different device sizes
   - Implement proper state management
   - Handle device permissions appropriately

2. **Code Quality**
   - Write clean, readable code
   - Avoid hardcoded values
   - Use dependency injection where appropriate
   - Follow object-oriented principles

3. **Performance**
   - Minimize unnecessary network calls
   - Optimize image and asset loading
   - Implement efficient data storage
   - Monitor and reduce memory usage

4. **User Experience**
   - Implement proper loading states
   - Add error handling with user-friendly messages
   - Design intuitive navigation flows
   - Consider accessibility features

Remember to connect your implementation to the Figma designs you've created and explain your technical decisions in your documentation.

---

## Türkçe

### Proje Genel Bakış

Bu klasör (`project/`), "Çözüm Sende" Hackathon için uygulama kaynak kodunuzu düzenleyeceğiniz yerdir. İyi yapılandırılmış bir proje organizasyonu, jürilerin çalışmanızı daha etkili bir şekilde değerlendirmesine yardımcı olacak ve teknik yeterliliğinizi gösterecektir.

### Beklenen Yapı

Projeniz aşağıdaki yapıya göre düzenlenmelidir:

```
📁 app/               (Uygulamanızın tüm kaynak kodu)
 ┣ 📁 lib/            (Ana uygulama kodu)
 ┣ 📁 assets/         (Görseller, fontlar ve diğer statik dosyalar)
 ┣ 📁 test/           (Birim ve entegrasyon testleri)
 ┗ 📄 pubspec.yaml    (Flutter için) veya eşdeğer yapılandırma dosyası
```

### Teknik Gereksinimler

1. **Kod Organizasyonu**
   - Standart mimari desenlerini takip edin (MVC, MVVM, Clean Architecture, vb.)
   - İlgi ayrımını koruyun
   - Uygun isimlendirme kurallarını kullanın
   - Uygun yorumlar ekleyin

2. **Kaynak Kontrolü**
   - Düzenli ve anlamlı commit'ler yapın
   - Gerekirse açıklayıcı dal (branch) isimleri kullanın
   - Tüm ekip üyelerinin depoya katkıda bulunmasını sağlayın

3. **Kalite Güvence**
   - Temel hata işleme mekanizmaları ekleyin
   - Farklı ekran boyutları için duyarlı tasarım uygulayın
   - Uygulama performansını mümkün olduğunca optimize edin
   - Kritik işlevler için birim testleri ekleyin (zaman izin verirse)

4. **Dokümantasyon**
   - Karmaşık mantığı açıklayan satır içi kod yorumları ekleyin
   - Mimari seçimlerinizi belgelendirin
   - README'nizde kurulum talimatları sağlayın

### Teknoloji Yığını

Bu onaylanmış mobil geliştirme yığınlarından birini seçin:

* **Çapraz Platform:** Flutter
* **iOS (Native):** Swift
* **Android (Native):** Kotlin

Aşağıdaki önerilen backend servislerinden herhangi birini kullanabilirsiniz:
* Firebase
* Supabase
* Appwrite

### En İyi Uygulamalar

1. **Mobil Geliştirme**
   - Platforma özgü tasarım kurallarını takip edin
   - Farklı cihaz boyutları için duyarlı düzenler sağlayın
   - Uygun durum yönetimini uygulayın
   - Cihaz izinlerini uygun şekilde yönetin

2. **Kod Kalitesi**
   - Temiz, okunabilir kod yazın
   - Sabit kodlanmış değerlerden kaçının
   - Uygun yerlerde bağımlılık enjeksiyonu kullanın
   - Nesne yönelimli prensipleri takip edin

3. **Performans**
   - Gereksiz ağ çağrılarını minimize edin
   - Görsel ve varlık yüklemesini optimize edin
   - Verimli veri depolama uygulayın
   - Bellek kullanımını izleyin ve azaltın

4. **Kullanıcı Deneyimi**
   - Uygun yükleme durumları uygulayın
   - Kullanıcı dostu mesajlarla hata işleme ekleyin
   - Sezgisel gezinme akışları tasarlayın
   - Erişilebilirlik özelliklerini göz önünde bulundurun

Uygulamanızı oluşturduğunuz Figma tasarımlarına bağlamayı ve dokümantasyonunuzda teknik kararlarınızı açıklamayı unutmayın.
