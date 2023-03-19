# SocialClub Bildirim Engelleyici

[Dutch](../NL/README.md) | [English](../../README.md) | [French](../FR/README.md) | [Romanian](../RO/README.md) | [Russian](../RU/README.md) | [Spanish](../ES/README.md) | Turkish

**16 Mart 2023 Güncellemesi: Bounty (ödül) bildirimleri istismarına neden olan kaynağı engellemek için #2 numaralı filtrenin üzerinde değişiklik yaptım.**

# [İndir v0.2.0](https://github.com/Speyedr/socialclub-notification-blocker/releases/download/v0.2.0/SocialClubBlocker-0.2.0.zip)

<img src="/img/SCBlockerTease1.png" alt="Main Menu" height=300 width=562>

## Kullanım
1. İndirin ve çıkarın (ya da kendiniz üretin). Bu mesajın üstünde, son birleştirilmiş yayına ait doğrudan indirme linki var.
2. `SCBlocker.exe` dosyasını Yönetici (Administrator) olarak çalıştırın.

    - Ek olarak, eğer Python kullanıyorsanız, repo dizinindeyken, yönetici haklarıyla açılmış bir komut satırında doğrudan `python main.py` komutunu yorumlayıcıdan çalıştırabilirsiniz.
      - Eğer bu yöntemi kullanırsanız, birleştirme ihtiyacı yoktur.
4. Eğer program çalışıyorsa ve ağ filterisi **AÇIKSA** (ON), bildirimler engelleniyor ve sizin istemcinize ulaşmıyor olmalı.
5. Menüde gezinmek için klavyenizdeki tuşları kullanın.

## Ayarlar
 - Otomatik olarak `config.ini` dosyasına kaydedilir. O dosyaya dokunmayın. Eğer dokunursanız ve program çökerse, dosyayı silip programı yeniden başlatın. Program varsayılan ayarlarına dönecektir.
 - Eğer `LOG BLOCKED ACTIVITY` (ENGELLEME HAREKETLİLİĞİNİ GÜNLÜĞE YAZ) **AÇIKSA** (ON), program, düşen veri paketlerinin bilgisini `debug.log` dosyasına günlükleyecektir. Eğer günlüğü gerçek zamanlı olarak izlemek istiyorsanız, [mTail](http://ophilipp.free.fr/op_tail.htm) gibi bir uygulama kullanabilirsiniz.

## Bildiriler
 - Bu program SocialClub Arayüzü'nü veya SocialClub Arayüzü etkin olarak çalışan hiçbir oyunu modifiye **etmez**. Teoride bunun anlamı, programın Rockstar'ın Hizmet Kullanım Şartları'nı ihlal etmediğidir.
 - Bu program tersine mühendislik yapılmış **hiçbir** kod içermediği gibi, Take-Two'nun fikri mülkiyetini veya telif hakkını ihlal eden kodlar da içermez.
 - Bu programı üretmek, Rockstar Games / Take-Two Interactive tarafından sağlanmış veya onlara bağlı olan **hiçbir** programın veya servisin çözülmesi ya da şifrelerinin kaldırılmasını gerektirmedi.

## Filtreler
 - Bu program, SocialClub Arayüzü ile sizin istemciniz arasındaki iletişim zincirinde bulunan farklı noktaları hedefleyen üç farklı deneysel filtreleme sağlıyor.
 - Filtre #1 `DROP_INC_80` en hızlısıdır ve performansı en az etkiler, fakat filtre kapatıldığında da bildirim yağmuruna tutulabilirsiniz.
 - Filtre #2 `DROP_CLIENT_POST` varsayılan olarak etkindir, çünkü alınan sonuç muhtemelen çoğu kullanıcının aradığı şeydir.
 - Filtre #3 `DROP_LENGTHS` en karmaşığıdır ve hala geliştirme aşamasındadır, bu yüzden tavsiye edilmez.

   <img src="/img/SCBlockerTease3.png" alt="Logging dropped packets" height=120 width=527>

## Buglar / Sorunlar
 - Eğer bir çökme ya da uygulamayı bozan bir bug ile karşılaşırsanız, lütfen talimatlara uyun ve [sorunu buraya yazın](https://github.com/Speyedr/socialclub-notification-blocker/issues/new/choose).

## Derleme Talimatları
**NOT:** Eğer kendiniz derlemeden sadece indirmek istiyorsanız, [Releases](https://github.com/Speyedr/socialclub-notification-blocker/releases) sayfasına gitmelisiniz. Ya da sadece sayfanın en üstünde bulunan "İndir" linkine tıklayın.
#### Windows

1) Python 3 (3.8+ tavsiye edilir) yükleyin

    - Eğer bu sizin ilk ve tek Python yüklemenizse, `Add Python to PATH` kutucuğunu işaretlemek sonraki adımı kolay hale getirir.
2) Aşağıdaki komutları Komut İstemi'nde çalıştırın:
```
:: Bu komutları çalıştırmadan önce, Komut İstemi'ni yerel repo dizininde açtığınızdan / yerel dizine geçtiğinizden emin olun.
C:\Users\Speyedr\socialclub-notification-blocker> pip install -r requirements.txt
:: Eğer 'pip' tanınmazsa (örneğin PATH'a eklenmemişse), pip.exe yolunu siz sağlamak zorundasınız.
:: Kesin yükleme yolunuzu kontrol ettiğinizden emin olun (versiyon numaranız veya paket farklı olabilir)
:: C:\Users\Speyedr\socialclub-notification-blocker> "C:\Program Files\Python 3.8\Scripts\pip.exe" install -r requirements.txt
C:\Users\Speyedr\socialclub-notification-blocker> python setup.py build
:: Yine, eğer python tanınmazsa, kesin yolu kullanmanız gerekebilir:
:: C:\Users\Speyedr\socialclub-notification-blocker> "C:\Program Files\Python 3.8\python.exe" setup.py build
```

## Emeği Geçenler

### Deney Fareleri

- [Wes0617](https://github.com/Wes0617)
- MrAlvie

### Tercümanlar

- [coeurGG](https://github.com/Ky0mie) (French)
- [Foxie117](https://github.com/Foxie1171) (Russian)
- [TKMachine](https://github.com/TKMachine) (Romanian)
- [Kyeki](https://github.com/Kyekii) (Spanish)
- [jorgex](https://github.com/jorgex94) (Spanish)
- [Rav1sh](https://github.com/Rav1sh) (Dutch)
- [Tmp341](https://github.com/Tmp341) (Turkish)

## BAĞIŞ
 - PayPal / Kart: [ko-fi.com/Speyedr](https://ko-fi.com/speyedr)
 - BTC: `347M8sHnahA98c7MjHGmvsb5pVUJeUcMZ5`
 - ETH: `0xDBAa338137Fc53BA007D7Cf99DD94908e8Fdb6d8`
 - ADA: `addr1qy6xlrpv43xjwhjpdvalccjxm3tf46f5cu7uh5uhexzgwyudcmm3ty8entef6tu3dgf8chn70tc3uql0kkrj0f62mw9sxh29w3`

## LİSANS
 - Bu programın kullanımı [GNU GPLv3.0 Lisansı](LICENSE) kapsamında sağlanır.

## KATKIDA BULUNMA
 - Eğer bir hata bulduysanız, yeni bir [sorun açarak](https://github.com/Speyedr/socialclub-notification-blocker/issues/new/choose) katkıda bulunabilirsiniz.
 - Pull request hareketleri şu anlık kapalıdır.
 - Bu projenin lisansı altında; tüm telif bildirilerini, bahsetmeleri, katkıda bulunanları ve türetilmiş işlerde bu programın lisansını koruduğunuz sürece, benim işime dayalı kendi sürümlerinizi yapmakta fazlasıyla özgürsünüz.