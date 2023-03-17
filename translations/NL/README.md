# SocialClub Notification Blocker

Dutch | [English](../../README.md) | [French](../FR/README.md) | [Romanian](../RO/README.md) | [Russian](../RU/README.md) | [Spanish](../ES/README.md) | [Turkish](../TR/README.md)



# [Download v0.2.0](https://github.com/Speyedr/socialclub-notification-blocker/releases/download/v0.2.0/SocialClubBlocker-0.2.0.zip)

<img src="/img/SCBlockerTease1.png" alt="Main Menu" height=300 width=562>

## Gebruik
1. Download en pak uit (of bouw zelf). De rechtstreekse downloadlink naar de laatst gecompileerde release staat boven dit bericht.
2. Voer `SCBlocker.exe` uit als administrator.

    - Als alternatief, als je Python hebt, kun je direct vanuit de interpreter werken door `python main.py` uit te voeren in een verhoogde command prompt terwijl je in de repo directory bent.
    - Als je deze methode gebruikt, is er geen build nodig.
4. Als het programma actief is en het netwerkfilter is **AAN**, meldingen zouden nu worden geblokkeerd en zullen de client niet meer bereiken.
5. Gebruik de toetsen op jouw toetsenbord om door het menu te navigeren.

## Configuratie
 - Slaat automatisch jouw instelling op in `config.ini`. Raak het niet aan. Als je het doet en het programma crasht, verwijder het bestand, start het programma opnieuw en het programma keert terug naar de standaardinstellingen.

 - Als `LOG BLOCKED ACTIVITY` is **ON**, het programma zal informatie over gedropte pakketten loggen in `debug.log`. Als je het log wilt bekijken in real-time, kun je gebruik maken van zoiets als [mTail](http://ophilipp.free.fr/op_tail.htm).



## Mededelingen
 - Dit programma wijzigt **niet** de SocialClub Overlay, noch enig andere spel dat wordt uitgevoerd met de SocialClub Overlay. In theroie, betekent dit dat dit programma niet de servicevoorwaarden van Rockstar schendt.
 - Dit programma bevat **geen** reverse-engineered code, noch enige code die de IP of het auteursrecht van Take-Two zou schenden.
 - Voor het maken van dit programma vereiste **geen** decompilatie of decodering van een programma of dienst geleverd door of gerelateerd aan Rockstar Games / Take-Two Interactive.

## Filters
 - Deze app biedt drie verschillende filterheuristieken die allemaal gericht zijn op verschillende punten in de communicatieketen tussen jouw client en de SocialClub-overlay.
 - Filter #1 `DROP_INC_80` is de snelste en heeft de minste invloed op de prestaties, maar je kunt worden overspoeld met meldingen wanneer het filter is uitgeschakeld.
 - Filter #2 `DROP_CLIENT_POST` is standaard ingeschakeld omdat het eindresultaat waarschijnlijk is waar de meeste gebruikers naar op zoek zijn.
 - Filter #3 `DROP_LENGTHS` is de meest gecompliceerde en nog in ontwikkeling en daarom niet aanbevolen.

   <img src="/img/SCBlockerTease3.png" alt="Logging dropped packets" height=120 width=527>

## Bugs / Problemen
 - Als je een crash of een andere applicatie-brekende bug tegenkomt, volg dan de instructies en [dien hier een probleem in](https://github.com/Speyedr/socialclub-notification-blocker/issues/new/choose).

## Bouw instructies
**OPMERKING:** Als je alleen naar de download zoekt zonder zelf te bouwen, moet je in plaats daarvan naar [Releases](https://github.com/Speyedr/socialclub-notification-blocker/releases) gaan. Of klik gewoon op de "Download" link bovenaan deze pagina.

#### Windows

1) Installeer Python 3 (3.8+ aanbevolen)

    - Als dit je eerste en enige Python-installatie is, zal het inschakelen van het selectievakje `Add Python to PATH` de volgende stap gemakkelijker maken.
2) Voer de volgende opdrachten uit in een command prompt:
```
:: Make sure to open the command prompt in / navigate to your local repo directory before running these commands.
C:\Users\Speyedr\socialclub-notification-blocker> pip install -r requirements.txt
:: If 'pip' is not recognised (i.e. it wasn't added to PATH) then you will need to provide the absolute path to pip.exe, e.g.
:: Make sure to check your exact install directory (your version number or bundle may be different)
:: C:\Users\Speyedr\socialclub-notification-blocker> "C:\Program Files\Python 3.8\Scripts\pip.exe" install -r requirements.txt
C:\Users\Speyedr\socialclub-notification-blocker> python setup.py build
:: Again, if python is not recognised then you will need to use the absolute path instead:
:: C:\Users\Speyedr\socialclub-notification-blocker> "C:\Program Files\Python 3.8\python.exe" setup.py build
```

## Credits

### Guinea Pigs

- [Wes0617](https://github.com/Wes0617)
- MrAlvie

### Vertalers

- [coeurGG](https://github.com/coeurGG) (French)
- [Foxie117](https://github.com/Foxie1171) (Russian)
- [TKMachine](https://github.com/TKMachine) (Romanian)
- [Kyeki](https://github.com/Kyekii) (Spanish)
- [jorgex](https://github.com/jorgex94) (Spanish)
- [Rav1sh](https://github.com/Rav1sh) (Dutch)

## DONEER
 - PayPal / Card: [ko-fi.com/Speyedr](https://ko-fi.com/speyedr)
 - BTC: `347M8sHnahA98c7MjHGmvsb5pVUJeUcMZ5`
 - ETH: `0xDBAa338137Fc53BA007D7Cf99DD94908e8Fdb6d8`
 - ADA: `addr1qy6xlrpv43xjwhjpdvalccjxm3tf46f5cu7uh5uhexzgwyudcmm3ty8entef6tu3dgf8chn70tc3uql0kkrj0f62mw9sxh29w3`

## LICENTIE
 - Gebruik van dit programma is beschikbaar gesteld onder de [GNU GPLv3.0 License](LICENSE).

## BIJDRAGEN
 - Als je een bug hebt gevonden, kun je  bijdragen door: [een probleem te openen](https://github.com/Speyedr/socialclub-notification-blocker/issues/new/choose).
 - Pull-verzoeken zijn momenteel gesloten.
 - Onder de voorwaarden van de licentie van dit project bent u meer dan welkom om uw eigen variaties te maken gebaseerd op mijn werk, zolang u alle copyrightvermeldingen, referenties, credits behoudt en ook de licentie van deze software gebruikt bij het vrijgeven van afgeleid werk.
