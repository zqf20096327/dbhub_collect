# Far Cry

![Far Cry Wallpaper](farcry_wallpaper_introduction.jpg)

## Introduction

[Far Cry is a first-person shooter (FPS) video game](https://www.youtube.com/watch?v=Cz3vGM08S7Q&has_verified=1) with amazing graphics, developed by Crytek and published by Ubisoft. The game was released in 2004 for Microsoft Windows and was a huge commercial success. Ubisoft closed the online servers almost 12 years later.

Far Cry features several [multiplayer modes](https://www.youtube.com/watch?v=GaFM0uWAzh0) in which players basically score points by killing other players. One of these multiplayer modes is deathmatch, also known as free for all (FFA), where the goal is to kill (or frag, from the military term) as many other players as possible within a limited period of time. Basically, everything that moves SHOULD be killed… :)

## Multiplayer FFA Session

Players can join an online multiplayer session by connecting to a Far Cry server. A session starts for a configurable limited period of time, for example: 30 minutes, during which each player tries their best to seek out and kill other players.

When the limited period of time expires, the game stops and it displays the results of the match as an ordered leaderboard with the number of kills and deaths per player, and the efficiency of each player:

![Multiplayer Match Session Leaderboard](farcry_multiplayer-match-session-leaderboard.jpg)

## Weapons

Players have access to a large arsenal of real-world weapons in Far Cry, from grenades and pistols, to rocket launchers, machines guns and sniper rifles. Check out [all of the weapons from good old Far Cry](https://www.youtube.com/watch?v=vzNG4VlCTFM)! They sound so cool!

| Name                                              | Code                                                  | Photo                                              |
| ------------------------------------------------- | ----------------------------------------------------- | -------------------------------------------------- |
| Machete                                           | `Machete`                                             | ![](farcry_weapon_machete.png)                     |
| Jungle Falcon                                     | `Falcon`                                              | ![](farcry_weapon_jungle-falcon.png)               |
| Jackhammer Shotgun                                | `Shotgun`                                             | ![](farcry_weapon_jackhammer-shotgun.png)          |
| P90 SMG                                           | `P90`                                                 | ![](farcry_weapon_p90-smg.png)                     |
| MP5 SMG                                           | `MP5`                                                 | ![](farcry_weapon_mp5-smg.png)                     |
| M4 Carbine                                        | `M4`                                                  | ![](farcry_weapon_m4-carbine.png)                  |
| AG36 Assault Rifle                                | `AG36` for the rifle, `AG36Grenade` for the explosive | ![](farcry_weapon_ag36-assault-rifle.png)          |
| OICW Advanced Assault Rifle                       | `OICW` for the rifle, `OICWGrenade` for the explosive | ![](farcry_weapon_oicw-advanced-assault-rifle.png) |
| AW50 Sniper Rifle                                 | `SniperRifle`                                         | ![](farcry_weapon_aw50-sniper-rifle.png)           |
| M249 SAW MG                                       | `M249`                                                | ![](farcry_weapon_m249-saw-mg.png)                 |
| Rocket Launcher                                   | `Rocket`                                              | ![](farcry_weapon_rocket-launcher.png)             |
| Grenade                                           | `HandGrenade`                                         | ![](farcry_weapon_grenade-mk2.jpg)                 |
| Mk.19 Mounted Mortar Launch

[...截断...]

er Platform            | `StickyExplosive`                                     | ![](farcry_weapon_mortar.jpg)                      |
| Patrol Boat (when a player runs over another)     | `Boat`                                                | ![](farcry_vehicle_patrol-boat.jpg)                |
| Humvee or Buggy (when a player runs over another) | `Vehicle`                                             | ![](farcry_vehicle_buggy.png)                      |
| Rocket Launcher mounted on a vehicle              | `VehicleMountedRocketMG`                              | ![](farcry_vehicle_humvee.png)                     |
| Mounted Minigun                                   | `VehicleMountedAutoMG`, `MG`                          | ![](farcry_weapon_vulcan-minigun.jpg)              |
| Machine Gun mounted on a vehicle                  | `VehicleMountedMG`                                    | ![](farcry_vehicle_buggy.png)                      |
| Rocket Launcher mounted on a vehicle              | `VehicleRocket`                                       | ![](farcry_vehicle_humvee.png)                     |

_Note: AG36 Assault Rifle and OICW Advanced Assault Rifle weapons have two fire modes: automatic rifle and grenade launcher._

## Server Log: Frag History

The Far Cry server stores [log information in a text file](./logs/log00.txt), starting with engine and system initialization data, followed by all the frags that occurred in every match sessions. For instance:

```bash
$ cat ./logs/log00.txt | grep killed | head
<26:32> <Lua> papazark killed lamonthe with AG36
<27:07> <Lua> theprophete killed lamonthe with Rocket
<27:18> <Lua> theprophete killed lamonthe with Rocket
<27:29> <Lua> theprophete killed lamonthe with Rocket
<27:47> <Lua> theprophete killed lamonthe with Rocket
<28:10> <Lua> theprophete killed papazark with Rocket
<28:49> <Lua> theprophete killed papazark with Rocket
<29:28> <Lua> papazark killed lamonthe with AG36
<29:36> <Lua> papazark killed lamonthe with AG36
<30:07> <Lua> theprophete killed papazark with SniperRifle
```

The format of a line corresponding to a frag, when a player kills one other player, is:

```text
<MM:SS:> <Lua> killer_username killed victim_username with weapon_code
```

or the following format, when a player kills himself, e.g., when a stupid player miserably dies by throwing a grenade that eventually explodes at their feet...

```text
<MM:SS:> <Lua> killer_username killed itself
```

Where:

- `MM`: zero-padded minute between 00 and 59 of the time when the frag occurred;
- `SS`: zero-padded second between 00 and 59 of the time when the frag occurred;
- `killer_username`: username of the player who fragged another; can only contain letters, numbers, dashes ("`-`"), periods ("`.`"), and underscores (`_`);
- `victim_username`: username of the player who has been fragged;
- `weapon_code`: code name of the weapon that was used to frag the other player.

_Note: The time of a frag is relative to the time the Far Cry engine started. It represents the number of minutes/seconds elapsed between the moment the game engine started and when the frags occurred._

_Note: Players who joined a match but who hid during all the match, meaning they didn't kill anyone and they haven't been killed by anyone, don't appear in the frag history at all. We just ignore them._

You can download [Far Cry 1.34 on Windows](https://drive.google.com/file/d/1pQ5RFuQ3t669KXd_jV-2KoOONdT6NcY8/view?usp=sharing), [unzip](https://www.7-zip.org/) the archive on the disk of your computer, and run the executable `./Bin32/FarCry.exe`.

![](farcry_wallpaper_00.jpg)

# Waypoint 1: Read Game Session Log File

Write a function `read_log_file` that takes an argument `log_file_pathname`, representing the pathname of a Far Cry server log file, and reads and returns all the bytes from the file.

For example:

```python
>>> log_data = read_log_file('./logs/log00.txt')
>>> len(log_data)
45633
```

# Waypoint 2: Parse Far Cry Engine's Start Time

The