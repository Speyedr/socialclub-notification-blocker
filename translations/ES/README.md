# SocialClub Notification Blocker

[Dutch](../NL/README.md) | [English](../../README.md) | [French](../FR/README.md) | [Romanian](../RO/README.md) | [Russian](../RU/README.md) | Spanish

**8 de marzo de 2022 ACTUALIZACION: Rockstar ha corregido el exploit del espectador.**

**Hice un anuncio sobre el mismo [futuro de SCBlocker](https://github.com/Speyedr/socialclub-notification-blocker/discussions/12).**

# [Descargar v0.1.1](https://github.com/Speyedr/socialclub-notification-blocker/releases/download/v0.1.1/SocialClubBlocker-0.1.1.zip)

<img src="/img/SCBlockerTease1.png" alt="Main Menu" height=300 width=562>

## Uso
1. Descargar y extraer (o compílelo usted mismo). El enlace directo de descarga a la última versión compilada se encuentra en la parte superior de este mensaje.
2. Ejecute `SCBlocker.exe` como administrador.

    - Alternativamente, si tiene Python, puede correr el programa directamente desde el intérprete al ejecutar `python main.py` en una línea de comandos como administrador mientras esté en el directorio del repositorio.
      - Si usa este método no es necesaria ninguna compilación adicional.
4. Si el programa está corriendo y el filtro de red está **ENCENDIDO**, las notificaciones deberían estar bloqueadas, por lo tanto, no llegarán al cliente.
5. Use las teclas en su teclado para navegar por el menú.

## Configuración
 - La configuración se  guarda automáticamente en `config.ini`. No toque ese archivo. Si lo hace y el programa se cuelga, borre el archivo, reinicie el programa y así el programa volverá al modo predeterminado.
 - Si el `REGISTRO DE ACTIVIDAD BLOQUEADA` está **ENCENDIDO**, el programa registrará la información de los paquetes perdidos en `debug.log`. Si quiere observar el registro en tiempo real, puede usar un programa como [mTail](http://ophilipp.free.fr/op_tail.htm).

## Avisos
 - Este programa **no** modifica la superposición de SocialClub, ni cualquier juego que funcione con el mismo. En teoría, significa que el programa no infringe los términos de servicio de Rockstar.
 - Este programa **no** contiene código de ingeniería inversa, ni ningún otro código que infrinja la propiedad intelectual o derechos de autor de Take-Two.
 - Crear este programa **no** requirió ninguna descompilación ni descifrado de ningún programa o servicio provisto o relacionado con Rockstar Games y/o Take-Two Interactive.

## Filtros
 - Este programa tiene tres técnicas de filtración distintas dirigidas a puntos distintos en la cadena de comunicación entre su cliente y la superposición de SocialClub.
 - Filtro #&#x2060;1 `DROP_INC_80` es el más rápido y el que menos afecta al rendimiento, pero puede sobrecargarse con notificaciones cuando el filtro se desactiva.
 - Filtro #&#x2060;2 `DROP_CLIENT_POST` es el filtro habilitado por defecto, ya que el resultado es posiblemente lo que la mayoría de los usuarios buscan.
 - Filtro #&#x2060;3 `DROP_LENGTHS` es el más complejo y todavía está en desarrollo. Por lo tanto su uso no está recomendado.

   <img src="/img/SCBlockerTease3.png" alt="Logging dropped packets" height=120 width=527>

## Bugs / Errores
 - Si encuentra algún error o bug que interfiera con la aplicación, por favor, siga las instrucciones y [publíquelo aquí](https://github.com/Speyedr/socialclub-notification-blocker/issues/new/choose).

## Instrucciones para compilarlo
**AVISO:** Si sólo está buscando la descarga directa que no necesita compilación, debe ir a [Releases](https://github.com/Speyedr/socialclub-notification-blocker/releases) o haga clic en el enlace de descarga de la parte superior de la página.
#### Windows

1) Instalar Python 3 (3.8+ es recomendado)

    - Si esta es su primera y única instalación de Python, al activar `Add Python to PATH` el siguiente paso será más fácil.
2) Ejecute el siguiente comando en la línea de comandos:
```
:: Asegúrese de que esté en el directorio del repositorio local antes de ejecutar estos comandos.
C:\Users\Speyedr\socialclub-notification-blocker> pip install -r requirements.txt
:: Si 'pip' no es reconocido (es decir, no fue agregado a PATH), entonces necesitará proporcionar la ruta completa a pip.exe. Debajo se brinda un ejemplo.
:: Asegúrese de comprobar el directorio de instalación (el suyo puede variar del ejemplo)  
:: C:\Users\Speyedr\socialclub-notification-blocker> "C:\Program Files\Python 3.8\Scripts\pip.exe" install -r requirements.txt
C:\Users\Speyedr\socialclub-notification-blocker> python setup.py build
:: De nuevo, si Python no es reconocido, entonces tendrás que usar la ruta completa:
:: C:\Users\Speyedr\socialclub-notification-blocker> "C:\Program Files\Python 3.8\python.exe" setup.py build
```

## Créditos

### Testers

- [Wes0617](https://github.com/Wes0617)
- MrAlvie

### Traductores

- [coeurGG](https://github.com/coeurGG) (French)
- [Foxie117](https://github.com/Foxie1171) (Russian)
- [TKMachine](https://github.com/TKMachine) (Romanian)
- [Kyeki](https://github.com/Kyekii) (Spanish)
- [jorgex](https://github.com/jorgex94) (Spanish)
- [Rav1sh](https://github.com/Rav1sh) (Dutch)

## Donativos
 - PayPal / Card: [ko-fi.com/Speyedr](https://ko-fi.com/speyedr)
 - BTC: `347M8sHnahA98c7MjHGmvsb5pVUJeUcMZ5`
 - ETH: `0xDBAa338137Fc53BA007D7Cf99DD94908e8Fdb6d8`
 - ADA: `addr1qy6xlrpv43xjwhjpdvalccjxm3tf46f5cu7uh5uhexzgwyudcmm3ty8entef6tu3dgf8chn70tc3uql0kkrj0f62mw9sxh29w3`

## Licencia
 - El uso de este programa está bajo la [Licencia GNU GPLv3.0 (en inglés)](LICENSE).

## Contribuir
 - Si ha encontrado un error, puede ayudar a contribuir al [crear una publicación](https://github.com/Speyedr/socialclub-notification-blocker/issues/new/choose).
 - Los "Pull requests" (peticiones para cambios de código) están cerrados.
 - Bajo los términos de la licencia de este proyecto, usted está invitado a modificar este programa siempre y cuando todos y cada uno de los avisos de derechos de autor, referencias y créditos sean conservados. También, al uso de la licensia de este programa al publicar algún trabajo derivado del mismo.