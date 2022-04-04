# SocialClub Notification Blocker

[Dutch](../NL/README.md) | [English](../../README.md) | French | [Romanian](../RO/README.md) | [Russian](../RU/README.md) | [Spanish](../ES/README.md)

**8 Mars 2022 MISE A JOUR: Rockstar a patch le problème du spectateur mode.**

**J'ai fait une annonce ici [Le futur de SCBlocker (bientôt traduit)](https://github.com/Speyedr/socialclub-notification-blocker/discussions/12).**

# [Download v0.1.1](https://github.com/Speyedr/socialclub-notification-blocker/releases/download/v0.1.1/SocialClubBlocker-0.1.1.zip)

<img src="/img/SCBlockerTease1.png" alt="Main Menu" height=300 width=562>

## Usage

1. Télécharger et extraire (vous pouvez le build vous-même). Le lien direct pour télécharger la dernière version du logiciel est au-dessus de ce message.
2. Lancez `SCBlocker.exe` en tant qu'administrateur.

	* Autrement, si vous avez Python installé, vous pouvez directement le lancer via l'interprète (cmd) en exécutant `python main.py` dans une invite de commande. (Qui nécessite plus de privilèges dans le dossier du repo)
	* Si vous utilisez cette méthode, aucun build n'est nécessaire.

3. Si le programme est en cours d'exécution, et le filtre est sur **ON**, les notifications devraient-être bloquées et ne vont pas atteindre votre client.

4. Utilisez les touches de votre clavier pour naviguer dans le menu.

## Configuration

* Sauvegarde automatique de vos paramètres dans le fichier `config.ini`. Ne le touchez pas. Si vous le faîtes, et que le programme crash, supprimez le fichier, et relancez le programme, celui-ci va directement remettre vos paramètres par défaut.
* Si `LOG BLOCKED ACTIVITY` est **ON**, le programme va "log" (enregistrer) les informations à propos des paquets perdus dans `debug.log`. Si vous voulez regarder les logs en temps réel, vous pouvez utiliser un logiciel comme [mTail](http://ophilipp.free.fr/op_tail.htm).

## Notices

* Ce programme ne modifie pas l'overlay SocialClub, ou n'importe quel jeu utilisant l'overlay SocialClub lorsqu'il est en cours d'exécution. En théorie, cela signifie que le programme ne viole pas les conditions d'utilisation de Rockstar.
* Ce programme ne contient aucun code qui a nécessité ou utilisé le "reverse-engineering", ou code qui pourrait violer le Copyright de Take-Two interactive.
* Créer ce programme n'a pas requiet la moindre décompilation ou le moindre décryptage du moindre programme ou service fourni ou relié à Rockstar Games / Take-Two Interactive.

## Filtres

* Cette application fournit trois différents filtres heuristiques qui ciblent les différents points dans la chaine de communication entre votre client et l'overlay SocialClub.
* Filtre #&#x2060;1 `DROP_INC_80` est le plus rapide et impacte les performances le moins, mais vous risquez d'être inondés de notifications lorsque le filtre n'est pas activé.
* Filtre #&#x2060;2 `DROP_CLIENT_POST` est activé par défaut, et c'est, probablement ce que la plupart des utilisateurs recherchent.
* Filtre #&#x2060;3 `DROP_LENGTHS` est le plus compliqué, et encore en développement, pour le moment, il n'est pas recommandé.

  <img src="/img/SCBlockerTease3.png" alt="Logging dropped packets" height=120 width=527>

## Bugs / Problemes

* Si vous rencontrez un crash, ou alors un bug qui casse l'application, merci de suivre les instructions et [de soumettre votre problème ici](https://github.com/Speyedr/socialclub-notification-blocker/issues/new/choose).

## Instructions pour le build

**NOTE**: Si vous êtes en train de chercher le téléchargement, sans vous-même faire le build, vous devez aller dans [Releases](https://github.com/Speyedr/socialclub-notification-blocker/releases) à la place. Ou juste cliquer sur "Download" au haut de cette page.

#### Windows

1. Installez Python 3 (3.8+ est recommandé)
	* Si c'est votre première installation python, activez la case "Add Python to PATH" rendra la prochaine étape plus facile.

2. Exécutez la commande suivante dans une invite de commande ;

```
:: Make sure to open the command prompt in / navigate to your local repo directory before running these commands.
C:\Users\Speyedr\socialclub-notification-blocker> pip install -r requirements.txt
:: If 'pip' is not recognised (i.e. it wasn't added to PATH) then you will need to provide the absolute path to pip.exe, e.g.
:: Make sure to check your exact install directory (your version number or bundle may be different)
:: C:\Users\Speyedr\socialclub-notification-blocker> "C:\Program Files\Python 3.8\Scripts\pip.exe" install -r requirements.txt
C:\Users\Speyedr\socialclub-notification-blocker> python setup.py build
:: Again, if python is not recognised then you will need to use the absolute path instead:
:: C:\Users\Speyedr\socialclub-notification-blocker> "C:\Program Files\Python 3.8\python.exe" setup.py build
}
```

## Credits

### Cochons d'Inde

* [Wes0617](https://github.com/Wes0617)
* MrAlvie

### Traduction / Translation

- [coeurGG](https://github.com/coeurGG) (French)
- [Foxie117](https://github.com/Foxie1171) (Russian)
- [TKMachine](https://github.com/TKMachine) (Romanian)
- [Kyeki](https://github.com/Kyekii) (Spanish)
- [jorgex](https://github.com/jorgex94) (Spanish)
- [Rav1sh](https://github.com/Rav1sh) (Dutch)

## DONATE

* PayPal / Card: [ko-fi.com/Speyedr](https://ko-fi.com/speyedr)
* BTC: `347M8sHnahA98c7MjHGmvsb5pVUJeUcMZ5`
* ETH: `0xDBAa338137Fc53BA007D7Cf99DD94908e8Fdb6d8`
* ADA: `addr1qy6xlrpv43xjwhjpdvalccjxm3tf46f5cu7uh5uhexzgwyudcmm3ty8entef6tu3dgf8chn70tc3uql0kkrj0f62mw9sxh29w3`

## LICENCE

* L'utilisation de ce programme est offert sous la [Licence GNU GPLv3.0](LICENSE).

## CONTRIBUTIONS 

* Si vous avez trouvé un bug, vous pouvez aider en [signalant un problème](https://github.com/Speyedr/socialclub-notification-blocker/issues/new/choose).
* Les demandes d'extraction sont actuellement fermées.
* Selon les termes de la licence de ce projet, vous êtes plus que bienvenu pour créer vos propres variations basées sur mon travail tant que vous conservez tous les avis de droit d'auteur, références, crédits et utilisez également la licence de ce logiciel lors de la publication de tout travail dérivé.