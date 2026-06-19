# SPF Spoofing Test

SPF Spoofing Test, bir alan adının e-posta sahteciliğine (email spoofing) karşı ne kadar dayanıklı olduğunu değerlendirmek amacıyla geliştirilmiş bir Python aracıdır. Araç, hedef alan adının SPF (Sender Policy Framework) yapılandırmasını kontrol eder ve SPF korumasının bulunmadığı veya yanlış yapılandırıldığı senaryolarda e-posta sunucularının bu durumu nasıl ele aldığını gözlemlemeye yardımcı olur.

Bu araç özellikle güvenlik araştırmacıları, sistem yöneticileri ve sızma testi uzmanları için geliştirilmiştir. SPF kaydının bulunmaması veya hatalı yapılandırılması durumunda saldırganlar alan adı sahibini taklit eden e-postalar gönderebilir. Bu durum kimlik avı (phishing), marka taklidi ve sosyal mühendislik saldırıları için ciddi bir risk oluşturur.

Araç yalnızca sahibi olduğunuz veya açık yetkiye sahip olduğunuz sistemlerde kullanılmalıdır.

---

# Özellikler

* SPF kaydı kontrolü
* MX kayıtlarının otomatik çözülmesi
* Hedef MX sunucusuna doğrudan teslimat desteği
* Özel gönderen adresi tanımlayabilme
* Özel konu ve içerik desteği
* SMTP kimlik doğrulama desteği
* TLS ve SSL desteği
* SPF eksikliği durumunda güvenlik önerileri
* Ayrıntılı SMTP hata çıktıları

---

# Gereksinimler

* Python 3.8 veya üzeri
* dnspython

---

# Kurulum

Gerekli bağımlılığı yükleyin:

```bash
pip install dnspython
```

Depoyu klonlayın:

```bash
git clone https://github.com/USERNAME/spf-spoof-test.git
cd spf-spoof-test
```

---

# Kullanım

Öncelikle göndermek istediğiniz e-posta içeriğini bir dosyada oluşturun:

```bash
cat > body.txt << 'EOF'
Hi there,

Party this Friday at 6pm!

See you!
EOF
```

Ardından aracı çalıştırın:

```bash
python3 spf_spoof_test.py \
    --domain keensafe.com \
    --to armenace@proton.me \
    --direct \
    --subject "Party" \
    --message "$(cat body.txt)"
```

Program çalıştırıldığında yetkinizin olup olmadığını doğrulamak amacıyla aşağıdaki soruyu soracaktır:

```text
Do you own 'keensafe.com' and have authorization to test this? (yes/no):
```

Yalnızca ilgili alan adı üzerinde test yapma yetkiniz varsa devam etmelisiniz.

---

# Parametreler

| Parametre        | Açıklama                                     |
| ---------------- | -------------------------------------------- |
| `--domain`       | Test edilecek alan adı                       |
| `--sender`       | Kullanılacak gönderen adresi                 |
| `--to`           | Alıcı e-posta adresi                         |
| `--direct`       | Mesajı doğrudan hedef MX sunucusuna gönderir |
| `--server`       | SMTP sunucusu                                |
| `--port`         | SMTP portu                                   |
| `--tls`          | STARTTLS kullanır                            |
| `--ssl`          | SSL kullanır                                 |
| `--user`         | SMTP kullanıcı adı                           |
| `--pass`         | SMTP parolası                                |
| `--subject`      | E-posta konusu                               |
| `--message`      | E-posta içeriği                              |
| `--timeout`      | Bağlantı zaman aşımı                         |
| `--no-spf-check` | SPF kontrolünü atlar                         |

---

# Kullanım Örnekleri

## Doğrudan MX Sunucusuna Gönderim

Bu yöntem hedef alan adının MX kayıtlarını çözerek mesajı doğrudan ilgili e-posta sunucusuna iletmeye çalışır.

```bash
python3 spf_spoof_test.py \
    --domain example.com \
    --to security@example.net \
    --direct \
    --subject "SPF Test" \
    --message "Authorized SPF security assessment."
```

---

## SMTP Sunucusu Kullanarak Gönderim

Kimlik doğrulaması gerektiren SMTP sunucuları için kullanılabilir.

```bash
python3 spf_spoof_test.py \
    --domain example.com \
    --to security@example.net \
    --server smtp.example.com \
    --port 587 \
    --tls \
    --user username \
    --pass password \
    --subject "SPF Test" \
    --message "Authorized SPF security assessment."
```

---

# Araç Nasıl Çalışır?

Araç öncelikle hedef alan adının SPF kaydını kontrol eder. Eğer SPF kaydı bulunamazsa kullanıcıya alan adının e-posta sahteciliğine karşı savunmasız olabileceği bilgisi verilir.

Ardından belirtilen alıcı adresinin MX kayıtları çözülür ve e-posta doğrudan ilgili posta sunucusuna gönderilmeye çalışılır. E-posta başlığında belirtilen gönderen adresi test edilen alan adı kullanılarak oluşturulur.

Bu süreç sayesinde e-posta altyapısının SPF eksikliği durumunda nasıl davrandığı gözlemlenebilir ve gerekli güvenlik önlemleri alınabilir.

---

# Örnek Çıktı

```text
============================================================
SPF SPOOFING TEST - FOR AUTHORIZED TESTING ONLY
============================================================

[!] Target domain: example.com
[!] Recipient: security@example.net

[*] Checking SPF record...

[+] Domain 'example.com' has NO SPF record - vulnerable to spoofing.

[*] Resolving MX for recipient domain 'example.net'...

[+] MX records for 'example.net':
    Priority 10: mail.example.net

[*] Delivering directly to MX: mail.example.net:25

[✓] Email sent successfully!
```

---

# Güvenlik Önerileri

Bir alan adının e-posta sahteciliğine karşı korunabilmesi için aşağıdaki mekanizmaların birlikte kullanılması önerilir.

## SPF

```txt
v=spf1 mx ~all
```

SPF, hangi sunucuların alan adınız adına e-posta göndermeye yetkili olduğunu belirtir.

---

## DKIM

DKIM, gönderilen e-postaların kriptografik olarak imzalanmasını sağlar ve mesajın değiştirilmediğini doğrular.

---

## DMARC

```txt
v=DMARC1; p=reject;
```

DMARC, SPF ve DKIM sonuçlarını değerlendirerek başarısız doğrulamalara karşı uygulanacak politikayı belirler.

---

# Sorumluluk Reddi

Bu yazılım yalnızca eğitim, araştırma ve yetkili güvenlik testleri amacıyla geliştirilmiştir.

Kullanıcılar aracı kullanmadan önce gerekli izinlere sahip olduklarından emin olmalıdır. Yazılımın kötüye kullanılması, izinsiz test faaliyetleri veya üçüncü taraf sistemlerde gerçekleştirilen işlemlerden doğabilecek hukuki ve teknik sonuçlardan kullanıcı sorumludur.

Yazar, yazılımın kullanımından kaynaklanabilecek herhangi bir zarar, veri kaybı, hizmet kesintisi veya yasal sorumluluktan yükümlü değildir.

---

# Lisans

Bu proje MIT Lisansı altında dağıtılmaktadır. Detaylar için `LICENSE` dosyasına bakabilirsiniz.
