# SocialClub Notification Blocker

[Dutch](../NL/README.md) | [English](../../README.md) | [French](../FR/README.md) | Romanian | [Russian](../RU/README.md) | [Spanish](../ES/README.md)

**8 Martie, 2022 UPDATE: Rockstar a reparat exploit-ul legat de modul spectator.**

**Am făcut un anunț despre [viitorul SCBlocker](https://github.com/Speyedr/socialclub-notification-blocker/discussions/12).**

# [Descarcă v0.1.1](https://github.com/Speyedr/socialclub-notification-blocker/releases/download/v0.1.1/SocialClubBlocker-0.1.1.zip)

<img src="/img/SCBlockerTease1.png" alt="Main Menu" height=300 width=562>

## Utilizare
1. Descarcă și extrage (sau compilează singur). Link-ul direct de descărcare către cea mai nouă versiune compilată este deasupra.
2. Rulează `SCBlocker.exe` cu drepturi de Administrator.

    - Alternativ, dacă ai Python, poți sa îl rulezi direct din interpretor executând `python main.py` într-un command prompt elevat cât timp te afli în directoriul repo.
      - Dacă folosești această metodă atunci nu este nevoie de un build.
4. Dacă programul rulează și filtru-l de internet este **ON**, notificările ar trebui să fie blocate și nu ar trebui să ajungă la clientul tău.
5. Folosește tastele pentru a naviga meniul.

## Configurație
 - Programul salvează automat setările în `settings.ini`. Nu te atinge de acest fișier. Dacă o faci și programul se blochează, șterge fișierul, restartează programul, și acesta va reveni la setările implicite.
 - Dacă `LOG BLOCKED ACTIVITY` este **ON**, programul va înregistra informația despre packet-uri pierdute în `debug.log`. Dacă dorești sa vizualizezi informația în timp real, poți să utilizezi un program precum [mTail](http://ophilipp.free.fr/op_tail.htm).

## Observații
 - Acest program **nu** modifică Overlay-ul SocialClub, nici alt program care rulează cu overlay-ul SocialClub. În teorie, acest lucru înseamnă că acest program nu incalcă Termenii Serviciului Rockstar's.
 - Acest program **nu** conține cod dedus prin inginerie inversă, nici orice alt fel de cod care ar putea incălca IP-ul companiei Take-Two sau copyright-ul ei.
 - Crearea acestui program **nu** a necesitat decompilarea sau decriptarea unui program sau serviciu furnizat sau relatat cu compania Rockstar Games/ Take-Two Interactive.

## Filtre
 - Această aplicație utilizează trei algoritmi diferiți care vizează differite puncte în lanțul de comunicări dintre clientul tău și overlay-ul SocialClub.
 - Filtrul #1 `DROP_INC_80` este cel mai rapid și afectează cel mai puțin performanța dar este posibil să fi surprasolicitat cu notificări când filtrul este oprit.
 - Filtrul #2 `DROP_CLIENT_POST` este pornit implicit din moment ce acesta indeplinește așteptările minime ale utilizatorului.
 - Filtrul #3 `DROP_LENGTHS` este cel mai complicat și încă în faza de dezvoltare, astfel acesta nu este recomandat.

   <img src="/img/SCBlockerTease3.png" alt="Logging dropped packets" height=120 width=527>

## Bug-uri / Probleme
 - Dacă intâmpini o eroare sau un bug care împiedică rularea aplicației, urmează instrucțiunile și [trimite informația aici](https://github.com/Speyedr/socialclub-notification-blocker/issues/new/choose).

## Instrucțiuni pentru compliare
**NOTĂ:** Dacă cauți doar să descarci programul fără al compila, trebuie sa mergi la [Versiuni](https://github.com/Speyedr/socialclub-notification-blocker/releases). Sau doar dă click pe linkul "Descarcă" de la vârful paginii.
#### Windows

1) Instalează Python 3 (3.8+ recomandat)
    - Dacă aceasta este prima și singura instalare a programului Python, activarea casetei de selectare `Add Python to PATH` va face pasul următor mult mai ușor.
2) Rulează următoarele comenzi într-un command prompt:
```
:: Asigură-te că ai deschis command prompt-ul în / navighează în directorul local al repo-ului înainte să rulezi comenzile.
C:\Users\Speyedr\socialclub-notification-blocker> pip install -r requirements.txt
:: Dacă 'pip' nu este recunoscut (e.x. nu a fost adăugat în PATH) atunci va trebui sa precizezi locația precisă pip.exe, e.x.
:: Asigură-te că ți-ai extras directorul de instalare (numărul versiunii sau al bundle-ului poate fi diferit)
:: C:\Users\Speyedr\socialclub-notification-blocker> "C:\Program Files\Python 3.8\Scripts\pip.exe" install -r requirements.txt
C:\Users\Speyedr\socialclub-notification-blocker> python setup.py build
:: Incă odată, dacă python nu este recunoscut atunci va trebui sa folosești locația precisă:
:: C:\Users\Speyedr\socialclub-notification-blocker> "C:\Program Files\Python 3.8\python.exe" setup.py build
```

## Credits

### Guinea Pigs

- [Wes0617](https://github.com/Wes0617)
- MrAlvie

### Translatori

- [coeurGG](https://github.com/coeurGG) (French)
- [Foxie117](https://github.com/Foxie1171) (Russian)
- [TKMachine](https://github.com/TKMachine) (Romanian)
- [Kyeki](https://github.com/Kyekii) (Spanish)
- [jorgex](https://github.com/jorgex94) (Spanish)
- [Rav1sh](https://github.com/Rav1sh) (Dutch)

## DONATI
 - PayPal / Card: [ko-fi.com/Speyedr](https://ko-fi.com/speyedr)
 - BTC: `347M8sHnahA98c7MjHGmvsb5pVUJeUcMZ5`
 - ETH: `0xDBAa338137Fc53BA007D7Cf99DD94908e8Fdb6d8`
 - ADA: `addr1qy6xlrpv43xjwhjpdvalccjxm3tf46f5cu7uh5uhexzgwyudcmm3ty8entef6tu3dgf8chn70tc3uql0kkrj0f62mw9sxh29w3`

## LICENȚĂ
 - Acest program este oferit sub licența [GNU GPLv3.0 License](LICENSE).

## CONTRIBUȚIE
 - Dacă ai descoperit un bug, poți să ajuți prin [deschiderea unui tichet](https://github.com/Speyedr/socialclub-notification-blocker/issues/new/choose).
 - Cererea de tragere este momentan inchisă.
 - Sub termenii de licență ai acestui proiect, sunteți bine veniți sa creați variați bazate pe lucrearea aceasta atât timp cât rețineți toate notițele referitoare la copyright, referințe, credit. Folosiți licența acestui software când lansați alte variați.