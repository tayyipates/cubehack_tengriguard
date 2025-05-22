
# Commit and PR Guidelines

## English

### Commit Guidelines

The commit type can include the following:

- [ ] feat – a new feature is introduced with the changes
- [ ] fix – a bug fix has occurred
- [ ] chore – changes that do not relate to a fix or feature and don't modify src or test files (for example updating dependencies)
- [ ] refactor – refactored code that neither fixes a bug nor adds a feature
- [ ] docs – updates to documentation such as a the README or other markdown files
- [ ] style – changes that do not affect the meaning of the code, likely related to code formatting such as white-space, missing semi-colons, and so on.
- [ ] test – including new or correcting previous tests
- [ ] perf – performance improvements
- [ ] ci – continuous integration related
- [ ] build – changes that affect the build system or external dependencies
- [ ] revert – reverts a previous commit
- [ ] add – when adding a new file, function, method, variable, and so on
- [ ] remove – when removing a file, function, method, variable, and so on
- [ ] update – when updating a file, function, method, variable, and so on
- [ ] rename – when renaming a file, function, method, variable, and so on
- [ ] move – when moving a file, function, method, variable, and so on
- [ ] copy – when copying a file, function, method, variable, and so on
- [ ] security – in case of vulnerabilities
- [ ] hotfix – a bug hot fix has occurred

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

- **type**: The type of change that this commit represents. A commit message must start with a type. Example: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `perf`, `ci`, `build`, `revert`, `add`, `remove`, `update`, `rename`, `move`, `copy`, `security`, `hotfix`.
- **scope**: A optional, lowercase noun describing a section of the codebase surrounded by parentheses, e.g. `api`, `cli`, `web`, `mobile`, `docs`, `tests`.
- **subject**: A brief summary of the changes made in the commit, written in the imperative mood (e.g., "add", "fix", "update").
- **body**: An optional, more detailed description of the changes, including the reasoning behind them and any relevant context. It should be separated from the subject by a blank line.
- **footer**: An optional section that can be used to reference any related issues or pull requests, breaking changes, or other important information. It should be separated from the body by a blank line.

### Examples

- **Feature commit**:
```
feat(api): add new endpoint for user registration

- added POST /api/register endpoint
- integrated email verification service
```

- **Bugfix commit**:
```
fix(cli): resolve issue with command not found

- updated command path in package.json
```

- **Documentation commit**:
```
docs: update README with installation instructions

- added step for installing dependencies
- clarified usage examples
```

- **Style commit**:
```
style(web): fix whitespace and indentation

- removed extra spaces in index.html
- fixed indentation in style.css
```

- **Refactor commit**:
```
refactor(mobile): restructure project folders

- moved components to src/components
- updated import paths
```

- **Test commit**:
```
test(api): add tests for user registration endpoint

- added tests for successful registration
- added tests for email verification
```

- **Performance commit**:
```
perf(web): optimize image loading

- compressed images in public/images
- implemented lazy loading for images
```

- **CI commit**:
```
ci: update GitHub Actions workflow

- added node.js 16 to CI matrix
- updated caching strategy
```

- **Build commit**:
```
build: upgrade dependencies

- upgraded webpack to version 5
- upgraded babel-loader to version 8
```

- **Revert commit**:
```
revert: revert "feat(api): add new endpoint for user registration"

This reverts commit 1234567.
```

- **Add commit**:
```
add: add CONTRIBUTING.md file

- added guidelines for contributing to the project
```

- **Remove commit**:
```
remove: remove unused images

- deleted old logo.png and background.jpg
```

- **Update commit**:
```
update: update package.json scripts

- added "lint": "eslint ."
- updated "test": "jest"
```

- **Rename commit**:
```
rename: rename component file

- renamed Button.js to MyButton.js
```

- **Move commit**:
```
move: move config file

- moved config.json to src/config
```

- **Copy commit**:
```
copy: copy README to docs

- copied README.md to docs/README.md
```

- **Security commit**:
```
security: update dependencies for security vulnerabilities

- updated lodash to version 4.17.21
- updated axios to version 0.21.1
```

- **Hotfix commit**:
```
hotfix(api): fix crash on user registration

- fixed null pointer exception in register function
```

## Turkish

### Commit Kuralları

Commit türü aşağıdakiler gibi olabilir:

- [ ] feat – değişikliklerle birlikte yeni bir özellik tanıtıldı
- [ ] fix – bir hata düzeltildi
- [ ] chore – bir düzeltme veya özellikle ilgisi olmayan ve src veya test dosyalarını değiştirmeyen değişiklikler (örneğin bağımlılıkları güncelleme)
- [ ] refactor – ne bir hatayı düzeltmeyen ne de bir özellik ekleyen yeniden yapılandırılmış kod
- [ ] docs – README veya diğer markdown dosyaları gibi belgelere yapılan güncellemeler
- [ ] style – kodun anlamını etkilemeyen, muhtemelen beyaz boşluk, eksik noktalı virgüller gibi kod biçimlendirmesi ile ilgili değişiklikler
- [ ] test – yeni testler ekleme veya önceki testleri düzeltme
- [ ] perf – performans iyileştirmeleri
- [ ] ci – sürekli entegrasyon ile ilgili
- [ ] build – derleme sistemini veya harici bağımlılıkları etkileyen değişiklikler
- [ ] revert – önceki bir commit'i geri alır
- [ ] add – yeni bir dosya, işlev, yöntem, değişken vb. eklenirken
- [ ] remove – bir dosya, işlev, yöntem, değişken vb. kaldırılırken
- [ ] update – bir dosya, işlev, yöntem, değişken vb. güncellenirken
- [ ] rename – bir dosya, işlev, yöntem, değişken vb. yeniden adlandırılırken
- [ ] move – bir dosya, işlev, yöntem, değişken vb. taşınırken
- [ ] copy – bir dosya, işlev, yöntem, değişken vb. kopyalanırken
- [ ] security – güvenlik açıkları durumunda
- [ ] hotfix – bir hata acil düzeltmesi yapıldığında

### Commit Mesajı Formatı

```
<type>(<scope>): <subject>

<body>

<footer>
```

- **type**: Bu commit'in temsil ettiği değişiklik türü. Bir commit mesajı bir tür ile başlamalıdır. Örnek: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `perf`, `ci`, `build`, `revert`, `add`, `remove`, `update`, `rename`, `move`, `copy`, `security`, `hotfix`.
- **scope**: Parantez içinde, kod tabanının bir bölümünü tanımlayan isteğe bağlı, küçük harfle yazılmış bir isim. Örneğin `api`, `cli`, `web`, `mobile`, `docs`, `tests`.
- **subject**: Değişikliklerin kısa bir özeti, emir kipiyle yazılmıştır (örneğin, "ekle", "düzelt", "güncelle").
- **body**: Değişikliklerin daha ayrıntılı bir açıklaması, arkasındaki mantık ve ilgili bağlam dahil. Konu ile arasında boş bir satır olmalıdır.
- **footer**: İsteğe bağlı bir bölüm, ilgili sorunları veya çekme isteklerini, kırılma değişikliklerini veya diğer önemli bilgileri referans göstermek için kullanılabilir. Gövde ile arasında boş bir satır olmalıdır.

### Örnekler

- **Özellik commit'i**:
```
feat(api): kullanıcı kaydı için yeni uç nokta ekle

- POST /api/register uç noktasını ekledi
- e-posta doğrulama hizmeti entegre edildi
```

- **Hata düzeltme commit'i**:
```
fix(cli): komut bulunamadı sorununu çöz

- package.json'daki komut yolunu güncelledim
```

- **Dokümantasyon commit'i**:
```
docs: README'yi kurulum talimatlarıyla güncelle

- bağımlılıkların nasıl yükleneceği adımını ekledi
- kullanım örneklerini netleştirdi
```

- **Biçim commit'i**:
```
style(web): boşluk ve girintiyi düzelt

- index.html'deki fazla boşlukları kaldırdı
- style.css'deki girintileri düzeltti
```

- **Yeniden yapılandırma commit'i**:
```
refactor(mobile): proje klasörlerini yeniden yapılandır

- bileşenleri src/components klasörüne taşıdı
- içe aktarma yollarını güncelledi
```

- **Test commit'i**:
```
test(api): kullanıcı kaydı uç noktası için testler ekle

- başarılı kayıt için testler eklendi
- e-posta doğrulama için testler eklendi
```

- **Performans commit'i**:
```
perf(web): resim yüklemeyi optimize et

- public/images klasöründeki resimleri sıkıştırdı
- resimler için tembel yükleme uygulandı
```

- **CI commit'i**:
```
ci: GitHub Actions iş akışını güncelle

- CI matrisine node.js 16 eklendi
- önbellekleme stratejisi güncellendi
```

- **Derleme commit'i**:
```
build: bağımlılıkları güncelle

- webpack'i 5. sürüme yükseltti
- babel-loader'ı 8. sürüme yükseltti
```

- **Geri alma commit'i**:
```
revert: "feat(api): kullanıcı kaydı için yeni uç nokta ekle" değişikliğini geri al

Bu, 1234567 numaralı commit'i geri alır.
```

- **Ekleme commit'i**:
```
add: CONTRIBUTING.md dosyasını ekle

- projeye katkıda bulunma yönergelerini ekledi
```

- **Kaldırma commit'i**:
```
remove: kullanılmayan resimleri kaldır

- eski logo.png ve background.jpg dosyalarını sildi
```

- **Güncelleme commit'i**:
```
update: package.json betiklerini güncelle

- "lint": "eslint ." eklendi
- "test": "jest" güncellendi
```

- **Yeniden adlandırma commit'i**:
```
rename: bileşen dosyasının adını değiştir

- Button.js dosyasını MyButton.js olarak yeniden adlandırdı
```

- **Taşıma commit'i**:
```
move: yapılandırma dosyasını taşı

- config.json dosyasını src/config klasörüne taşıdı
```

- **Kopyalama commit'i**:
```
copy: README'yi docs klasörüne kopyala

- README.md dosyasını docs/README.md olarak kopyaladı
```

- **Güvenlik commit'i**:
```
security: güvenlik açıkları için bağımlılıkları güncelle

- lodash'ı 4.17.21 sürümüne güncelledi
- axios'u 0.21.1 sürümüne güncelledi
```

- **Acil düzeltme commit'i**:
```
hotfix(api): kullanıcı kaydındaki çökme sorununu düzelt

- kayıt işlevindeki null pointer istisnasını düzeltti
```