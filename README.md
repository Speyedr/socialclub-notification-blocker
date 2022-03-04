# SocialClub Notification Blocker
Next-generation firewall (NGFW) that supports blocking SocialClub Overlay notifications.

![Main Menu](/img/SCBlockerTease1.png)

### Download (TODO)

## Usage
1. Download and extract (or build yourself).
2. Run `SCBlocker.exe` as Administrator.
3. If the program is running and the network filter is **ON**, notifications should now be blocked and won't reach your client.
4. Use the keys on your keyboard to navigate the menu.

## Configuration
 - Automatically saves your settings at `settings.ini`. Don't touch it. If you do and the program crashes, delete the file, restart the program, and the program will revert to defaults.
 - If enabled, will log information about dropped packets in `debug.log`. If you want to watch the log in real-time, you can use something like [mTail](http://ophilipp.free.fr/op_tail.htm) (no affiliation).

## Notices
 - This program does **not** modify the SocialClub Overlay, nor any game that runs with the SocialClub Overlay enabled. In theory, this means that this program does not violate Rockstar's Terms of Service.
 - This program does **not** contain any reverse-engineered code, nor any code that would violate Take-Two's IP or Copyright.
 - Creating this program did **not** require any decompilation nor decryption of any program or service provided by or related to Rockstar Games / Take-Two Interactive.

## Filters
 - This app provides three different filtering heuristics that all target different points in the chain of communication between your client and the SocialClub Overlay.
 - Filter #2 is enabled by default as the end result is probably what most users are looking for. Filter #1 is much faster and impacts performance less but you will be flooded with notifications when the filter is turned off.

![Logging dropped packets](/img/SCBlockerTease3.png)

## Bugs / Issues
 - If you encounter a crash or otherwise application-breaking bug, please follow the instructions and submit an Issue here. (TODO)

## Build instructions
 - `pip install requirements.txt`
 - `python setup.py build`

## DONATE
 - https://ko-fi.com/speyedr
 - 

## LICENSE
 - Use of this program is offered under the [GNU GPLv3.0 license](https://github.com/Speyedr/socialclub-notification-blocker/blob/main/LICENSE).

## CONTRIBUTING
 - Currently, contributions to this project will not be accepted. However,
 - Under terms of this project's license, you are more than welcome to create your own variations based on my work so long as you retain any copyright notices, references, credits, and this software's license.
