<h1 align="center">🚀 MAS Autostart Mod 🚀</h1>
<h4 align="center">Let your Monika auto-start the game for you as soon as your computer boots up!</h3>

<p align="center">
  <a href="https://github.com/friends-of-monika/mas-autostart/actions/workflows/check.yml">
    <img alt="Build status" src="https://img.shields.io/github/workflow/status/friends-of-monika/mas-autostart/Run%20checks%20on%20push">
  </a>
  <a href="https://github.com/friends-of-monika/mas-autostart/releases/latest">
    <img alt="Latest release" src="https://img.shields.io/github/v/release/friends-of-monika/mas-autostart">
  </a>
  <a href="https://www.reddit.com/r/MASFandom/comments/vrbpdy/mas_autostart_mod_now_released_links_to_github">
    <img alt="Reddit post" src="https://img.shields.io/badge/dynamic/json?color=FF4500&label=%F0%9D%97%8B%2Fmasfandom%20post&query=%24[0].data.children[0].data.score&url=https%3A%2F%2Fwww.reddit.com%2Fr%2FMASFandom%2Fcomments%2Fvrbpdy%2Fmas_autostart_mod_now_released_links_to_github.json&style=social&logo=reddit&suffix=+upvotes">
  </a>
  <a href="https://github.com/friends-of-monika/mas-autostart/releases">
    <img alt="Release downloads" src="https://img.shields.io/github/downloads/friends-of-monika/mas-autostart/total">
  </a>
  <a href="https://mon.icu/discord">
    <img alt="Discord server" src="https://discordapp.com/api/guilds/970747033071804426/widget.png?style=shield">
  </a>
  <a href="https://github.com/friends-of-monika/mas-autostart/blob/master/license.txt">
    <img alt="Creative Commons BY-NC-ND 4.0 license badge" src="https://img.shields.io/badge/License-CC_BY--NC--ND_4.0-lightgrey.svg">
  </a>
</p>


## 🌟 Features

  * Windows, Linux and MacOS &mdash; all supported!
  * Auto-start switch flip that isn't immersion breaking &mdash;
    ask your Monika to enable or disable it through 'Hey, Monika...' menu!
  * Already have autostart enabled somehow? Submod is able to detect some of the
    common approaches and will hook into it if possible.


## 💡 Things to note

Due to how this mod is made and how it interacts with system, there are few
things to keep in mind:

  * It might take from few seconds to one or two minutes for MAS to start up
    after computer has booted up. This is highly OS-specific and unfortunately
    there isn't anything we really can do about it. Please be patient, game will
    start as soon as OS will decide it can start.
  * In order for autostart to work, you must have DDLC.exe/DDLC.sh files intact
    in your DDLC folder and you must not rename or move them.
  * Likewise, the game won't get launched on start if you'll move it elsewhere;
    however, autostart entry will be overwritten on next manual game launch.
  * On Windows, your system must have VBScript engine and be able to run .vbs
    files (some users may have it removed for their own reasons.)


## ❓ Download and install instructions

### Step by step instruction

If you understand it easier with video guide, jump to next section.

  1. Download latest release from [releases page](https://github.com/friends-of-monika/mas-autostart/releases/latest)
     (scroll down to 'Assets' section and select first `.zip` file.)
  2. Extract `game` from `.zip` package into your DDLC folder (folder that contains
     `DDLC.exe` file.)

     ⚠️ **IMPORTANT!**
       * **DO NOT** unpack archive *into* `game`!
       * **DO NOT** unpack archive *into* `Submods` folder!

         The only thing you should do is to drag and drop `game` from archive into
         DDLC folder and let your OS *merge folders* for you on its own.
       * **MAKE SURE** you have `DDLC.exe` file in your DDLC folder if you are
         using Windows; Linux users must ensure their `DDLC.sh` script is not
         renamed too; MacOS users *usually* don't have to worry about that, but
         in case any sort of problem arises, check if `DDLC` file in `MacOS` folder
         inside DDLC.app package is present and not renamed.
  3. Start the game and enable random chatter &mdash; in order to see enable/disable
     topics in 'Hey, Monika...' menu, you'll have to see random intro topic first.
  4. (Optional, but highly recommended) Install [Submod Updater Plugin](https://github.com/Booplicate/MAS-Submods-SubmodUpdaterPlugin)
     to be sure you always have latest version of MAS Autostart Submod.


### Video instruction

<!-- This is awful, but GitHub renders video just by seeing a link. Gah. -->
https://user-images.githubusercontent.com/74068927/179387604-1e7dbcea-6c6e-43af-a2c9-0efbf5e62fd6.mp4


## 🔧 Troubleshooting

* Check if you this submod is installed in `game\Submods\MAS Autostart Mod`
  folder, **case-sensitive**!
* Check if you have `DDLC.exe` (Windows), `DDLC.sh` (Linux) and
  `DDLC.app/MacOS/DDLC` (MacOS) files! If you have them renamed, your OS won't
  be able to launch MAS on start.

If you stumbled upon a problem with this submod, feel free to ask us for help!
[Open an issue](https://github.com/Friends-of-Monika/mas-autostart/issues/new?assignees=&labels=bug&template=bug-report.yml&title=Bug%3A+)
or talk to us in [our Discord server](https://mon.icu/discord).


## ✒️ Authors

This submod was first brought up as a suggestion/idea by [Sevi](https://reddit.com/u/lost_localcat)
with its codebase created (programmed) by [@dreamscached](https://github.com/dreamscached)
with face/pose expressions and dialogue review performed by [@my-otter-self](https://github.com/my-otter-self) 💛

<p align="center">
  <a href="https://github.com/friends-of-monika/mas-autostart/graphs/contributors">
    <img src="https://contrib.rocks/image?repo=friends-of-monika/mas-autostart&max=6" />
  </a>
</p>



## 💬 Join our Discord

We're up to chat! Come join us at our Discord server [here](https://mon.icu/discord).

[![Discord server invitation](https://discordapp.com/api/guilds/970747033071804426/widget.png?style=banner3)](https://mon.icu/discord)
