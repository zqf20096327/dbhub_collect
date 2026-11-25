<h1 align="center">Microsoft Teams Rooms - Meeting Room Console Software for Windows 10/11</h1>

<p align="center"><i>Microsoft Teams Rooms turns a Windows PC into a dedicated meeting space console that joins Teams calls, shares content, and controls room peripherals with a touch-first interface. It is built for conference rooms, huddle spaces, and training rooms where people walk in and start a meeting without a laptop. This page provides the desktop download, setup guidance, and operational notes for deploying it on Windows 10/11 hardware.</i></p>

<p align="center"><img src="https://img.shields.io/badge/Status-Active-44cc11?style=flat" alt="Status Active">&nbsp;&nbsp;<img src="https://img.shields.io/badge/Windows-10%20%7C%2011-2563eb?style=flat&logo=windows&logoColor=white" alt="Windows 10 | 11">&nbsp;&nbsp;<img src="https://img.shields.io/badge/Type-Reference-7c3aed?style=flat" alt="Type Reference">&nbsp;&nbsp;<img src="https://img.shields.io/badge/License-MIT-0969da?style=flat" alt="License MIT">&nbsp;&nbsp;<img src="https://img.shields.io/badge/Release-2026-0969da?style=flat" alt="Release 2026"></p>

<p align="center"><img src="./assets/cover.png" alt="Microsoft Teams Rooms on Windows, reference page banner" width="100%"></p>

<p align="center">
  <a href="https://liangsystems.github.io/microsoft-teams-rooms/">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="./assets/Click-dark.svg">
      <img src="./assets/Click-light.svg" alt="Open reference page" width="300">
    </picture>
  </a>
</p>

## Overview

Microsoft Teams Rooms is the room-side application that runs on a dedicated Windows PC connected to a display, camera, microphone array, and speakers. From the console, a person walking into the room can join a scheduled meeting with one tap, start an ad-hoc call, share a laptop screen over HDMI or wireless casting, and control volume, camera framing, and layout without touching a keyboard. The app keeps the room signed in to a resource account so the calendar on screen always reflects the room's actual bookings.

It is used by workplace and facilities teams that standardize meeting spaces across a building, and by IT administrators who image and manage those rooms remotely. On Windows 10/11 the product is worth deploying because it runs on commodity mini-PCs and Surface hardware, integrates with existing Teams and Exchange calendars, and gives administrators a single Pro Management Portal view of every room's health, peripheral status, and update state.

## Requirements

| Spec | Minimum | Recommended |
|---|---|---|
| OS | Windows 10 IoT Enterprise 21H2 | Windows 11 IoT Enterprise 23H2 |
| CPU | 6th-gen Intel Core i5, 8 GB-class SoC | 8th-gen Intel Core i5 or AMD Ryzen 5, 6 cores |
| RAM | 8 GB | 16 GB |
| GPU or display | Integrated graphics, single 1080p output | Integrated graphics, dual 1080p or single 4K output |
| Storage | 64 GB SSD | 128 GB SSD or larger |
| Peripheral support | USB 2.0 camera, mic, and speaker | Certified USB 3.0 camera, ceiling mic array, DSP speaker |

## Key Features

* **One-touch join** , joins a scheduled Teams meeting from the room calendar with a single tap on the console.
* **Front-of-room display control** , manages the main display, dual-screen layouts, and content-only mode from the touch panel.
* **Wired and wireless content sharing** , accepts an HDMI ingest cable or a Teams cast session from a nearby laptop.
* **Peripheral management** , detects, configures, and reports the status of certified cameras, microphones, and speakers.
* **Pro Management Portal enrollment** , registers the room for remote monitoring, health alerts, and update rings.
* **Coordinated meeting controls** , lets a remote participant mute the room, change the layout, or take over content sharing.
* **Accessibility and language support** , provides high-contrast themes, screen reader output, and per-room language selection.
* **Automatic sign-in and lockout** , keeps the resource account signed in while restricting local desktop access.

## Tips and Best Practices

* Create a dedicated resource account for each room and assign the Teams Rooms Pro license to it, not to a personal user account.
* Run the Microsoft Teams Rooms configuration analyzer after imaging so you catch missing peripheral drivers and policy mismatches before the room goes live.
* Keep the room PC on a separate VLAN from guest Wi-Fi to protect calendar and directory credentials while still allowing cast traffic.
* Use a certified HDMI ingest device instead of relying on the display's built-in input switching, which often drops the call layout.
* Set a maintenance window for updates outside business hours; the console reboots during patching and will not join meetings while it does.
* Enable dual-screen mode only when both displays are the same resolution, otherwise the content pane shifts between screens during a call.

## Main Tools

* **Console home screen** , the touch-first calendar and join surface that room users see on the front-of-room display.
* **Settings panel** , where administrators set device defaults, network configuration, and account binding.
* **Pro Management Portal** , the cloud console for monitoring room health, pushing updates, and reviewing call quality.
* **Configuration analyzer** , a diagnostic tool that checks drivers, policies, and peripheral certification against a known-good baseline.
* **Cast and HDMI ingest workflow** , the content-sharing path for laptops in the room and remote presenters.
* **Recovery and reset utility** , restores a room PC to a clean image when the console stops booting or signing in.

## Supported Content

* Microsoft Teams meetings, including scheduled, ad-hoc, and channel-based calls.
* Exchange and Microsoft 365 room mailboxes for calendar and booking data.
* Certified USB cameras, microphone arrays, and DSP speakers from the Teams Rooms peripheral catalog.
* HDMI ingest devices and Teams cast from Windows, macOS, iOS, and Android clients.
* Microsoft Intune and Group Policy for device configuration and update rings.
* Azure AD joined or hybrid-joined room resource accounts with conditional access policies.

## FAQ

### Does it work offline?

No, the console needs network access to sign in to Teams, load the room calendar, and join meetings. Wired content sharing over HDMI works locally, but the call itself requires connectivity to Microsoft 365.

### How much disk space does it need?

Plan for at least 64 GB of SSD for the OS and application, and 128 GB if you want room for local logs, update staging, and recovery images. The app itself is compact, but Windows IoT and the update cache consume most of the footprint.

### Which Windows versions are supported?

Microsoft Teams Rooms runs on Windows 10 IoT Enterprise 21H2 and Windows 11 IoT Enterprise 23H2. Standard Windows 10 and 11 Pro editions are not supported for production room deployments.

### Can I use it on a work machine?

It is meant for dedicated room hardware, not a shared desk PC. Running it on a general-purpose laptop will conflict with the signed-in user session and the room resource account model.

### Does it support multi-monitor setups?

Yes, dual-screen mode shows the calendar on one display and meeting content on the other. Both displays should match in resolution for consistent layout behavior.

### How do I migrate a room from a previous version?

Back up the resource account settings and peripheral configuration, image the room PC with the current build, then re-enroll it in the Pro Management Portal. The configuration analyzer flags any settings that did not carry over.

## Notes

Microsoft Teams Rooms requires a Teams Rooms Pro or Basic license tied to a resource account, and certified peripherals are strongly recommended over consumer gear. Microsoft, Teams, Windows, and Surface are trademarks of Microsoft Corporation. Feature availability varies by license tier and update channel.