# SocialClub Notification Blocker
Next-generation firewall (NGFW) that supports blocking SocialClub Overlay notifications.

<img src="/img/SCBlockerTease1.png" alt="Main Menu" height=300>

### Download v0.1 (TODO)

## Usage
1. Download and extract (or build yourself).
2. Run `SCBlocker.exe` as Administrator.
3. If the program is running and the network filter is **ON**, notifications should now be blocked and won't reach your client.
4. Use the keys on your keyboard to navigate the menu.

## Configuration
 - Automatically saves your settings at `settings.ini`. Don't touch it. If you do and the program crashes, delete the file, restart the program, and the program will revert to defaults.
 - If `LOG BLOCKED ACTIVITY` is **ON**, the program will log information about dropped packets in `debug.log`. If you want to watch the log in real-time, you can use something like [mTail](http://ophilipp.free.fr/op_tail.htm).

## Notices
 - This program does **not** modify the SocialClub Overlay, nor any game that runs with the SocialClub Overlay enabled. In theory, this means that this program does not violate Rockstar's Terms of Service.
 - This program does **not** contain any reverse-engineered code, nor any code that would violate Take-Two's IP or Copyright.
 - Creating this program did **not** require any decompilation nor decryption of any program or service provided by or related to Rockstar Games / Take-Two Interactive.

## Filters
 - This app provides three different filtering heuristics that all target different points in the chain of communication between your client and the SocialClub Overlay.
 - Filter #2 `DROP_CLIENT_POST` is enabled by default as the end result is probably what most users are looking for.
 - Filter #1 `DROP_INC_80` is much faster and impacts network performance less but you will be flooded with notifications when the filter is turned off.
 - Filter #3 `DROP_LENGTHS` is the most complicated and still under development and therefore not recommended.

   <img src="/img/SCBlockerTease3.png" alt="Logging dropped packets" height=175>

## Bugs / Issues
 - If you encounter a crash or otherwise application-breaking bug, please follow the instructions and [submit an issue here](https://github.com/Speyedr/socialclub-notification-blocker/issues/new/choose).

## Build instructions
 - `pip install requirements.txt`
 - `python setup.py build`

## DONATE
 - PayPal / Card: [ko-fi.com/Speyedr](https://ko-fi.com/speyedr)
 - BTC: `347M8sHnahA98c7MjHGmvsb5pVUJeUcMZ5`
 - ETH: `0xDBAa338137Fc53BA007D7Cf99DD94908e8Fdb6d8`
 - ADA: `addr1qy6xlrpv43xjwhjpdvalccjxm3tf46f5cu7uh5uhexzgwyudcmm3ty8entef6tu3dgf8chn70tc3uql0kkrj0f62mw9sxh29w3`

## LICENSE
 - Use of this program is offered under the [GNU GPLv3.0 License](LICENSE).

## CONTRIBUTING
 - Currently, contributions to this project will not be accepted. However,
 - Under terms of this project's license, you are more than welcome to create your own variations based on my work so long as you retain any and all copyright notices, references, credits, and also use this software's license when releasing any derivative work.
