# SocialClub Notification Blocker

### [Download v0.1.0](https://github.com/Speyedr/socialclub-notification-blocker/releases/download/v0.1.0/SocialClubBlocker-0.1.0.zip)

<img src="/img/SCBlockerTease1.png" alt="Main Menu" height=300 width=562>

## Usage
1. Download and extract (or build yourself).
2. Run `SCBlocker.exe` as Administrator.

    - Alternatively, if you have Python, you can run directly from the interpreter by executing `python main.py` in an elevated command prompt while at the repo directory.
      - If you use this method then no build is needed.
4. If the program is running and the network filter is **ON**, notifications should now be blocked and won't reach your client.
5. Use the keys on your keyboard to navigate the menu.

## Configuration
 - Automatically saves your settings at `settings.ini`. Don't touch it. If you do and the program crashes, delete the file, restart the program, and the program will revert to defaults.
 - If `LOG BLOCKED ACTIVITY` is **ON**, the program will log information about dropped packets in `debug.log`. If you want to watch the log in real-time, you can use something like [mTail](http://ophilipp.free.fr/op_tail.htm).

## Notices
 - This program does **not** modify the SocialClub Overlay, nor any game that runs with the SocialClub Overlay enabled. In theory, this means that this program does not violate Rockstar's Terms of Service.
 - This program does **not** contain any reverse-engineered code, nor any code that would violate Take-Two's IP or Copyright.
 - Creating this program did **not** require any decompilation nor decryption of any program or service provided by or related to Rockstar Games / Take-Two Interactive.

## Filters
 - This app provides three different filtering heuristics that all target different points in the chain of communication between your client and the SocialClub Overlay.
 - Filter #1 `DROP_INC_80` is the fastest and impacts performance the least but you may be flooded with notifications when the filter is turned off.
 - Filter #2 `DROP_CLIENT_POST` is enabled by default as the end result is probably what most users are looking for.
 - Filter #3 `DROP_LENGTHS` is the most complicated and still under development and therefore not recommended.

   <img src="/img/SCBlockerTease3.png" alt="Logging dropped packets" height=120 width=527>

## Bugs / Issues
 - If you encounter a crash or otherwise application-breaking bug, please follow the instructions and [submit an issue here](https://github.com/Speyedr/socialclub-notification-blocker/issues/new/choose).

## Build Instructions
#### Windows

1) Install Python 3 (3.8+ recommended)

    - If this is your first and only Python install, enabling the check-box `Add Python to PATH` will make the next step easier.
2) Run the following commands in a command prompt:
```
:: Make sure to open the command prompt in / navigate to your local repo directory before running these commands.
C:\Users\Speyedr\socialclub-notification-blocker> pip install requirements.txt
:: If 'pip' is not recognised (i.e. it wasn't added to PATH) then you will need to provide the absolute path to pip.exe, e.g.
:: Make sure to check your exact install directory (your version number or bundle may be different)
:: C:\Users\Speyedr\socialclub-notification-blocker> "C:\Program Files\Python 3.8\Scripts\pip.exe" install requirements.txt
C:\Users\Speyedr\socialclub-notification-blocker> python setup.py build
:: Again, if python is not recognised then you will need to use the absolute path instead:
:: C:\Users\Speyedr\socialclub-notification-blocker> "C:\Program Files\Python 3.8\python.exe" setup.py build
```

## Credits

### Guinea Pigs

- [Wes0617](https://github.com/Wes0617)
- MrAlvie


## DONATE
 - PayPal / Card: [ko-fi.com/Speyedr](https://ko-fi.com/speyedr)
 - BTC: `347M8sHnahA98c7MjHGmvsb5pVUJeUcMZ5`
 - ETH: `0xDBAa338137Fc53BA007D7Cf99DD94908e8Fdb6d8`
 - ADA: `addr1qy6xlrpv43xjwhjpdvalccjxm3tf46f5cu7uh5uhexzgwyudcmm3ty8entef6tu3dgf8chn70tc3uql0kkrj0f62mw9sxh29w3`

## LICENSE
 - Use of this program is offered under the [GNU GPLv3.0 License](LICENSE).

## CONTRIBUTING
 - If you have found a bug, you can help contribute by [opening an issue](https://github.com/Speyedr/socialclub-notification-blocker/issues/new/choose).
 - Pull requests are currently closed.
 - Under terms of this project's license, you are more than welcome to create your own variations based on my work so long as you retain any and all copyright notices, references, credits, and also use this software's license when releasing any derivative work.
