<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./docs/assets/logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="./docs/assets/logo-light.svg">
    <img alt="A photo organizer for your file system without sticking to any application or vendor" src="./docs/assets/logo-light.svg">
  </picture>
</p>

[![Nuget release](https://img.shields.io/nuget/v/photo-cli?label=stable&color=blue)](https-://www.nuget.org/packages/photo-cli/) [![Nuget download count](https://img.shields.io/nuget/dt/photo-cli)](https://www.nuget.org/packages/photo-cli/) [![Docker Image Version](https://img.shields.io/docker/v/photocli/photocli?label=docker&logo=docker&logoColor=white)](https://hub.docker.com/r/photocli/photocli) [![Homebrew](https://img.shields.io/nuget/v/photo-cli?label=homebrew&color=yellow)](https://github.com/photo-cli/homebrew-photo-cli) [![Coverage](https://sonarcloud.io/api/project_badges/measure?project=photo-cli_photo-cli&metric=coverage)](https://sonarcloud.io/summary/new_code?id=photo-cli_photo-cli) [![.github/workflows/CI.yml](https://github.com/photo-cli/photo-cli/actions/workflows/CI.yml/badge.svg)](https://github.com/photo-cli/photo-cli/actions/workflows/CI.yml) [![.github/workflows/stable.yml](https://github.com/photo-cli/photo-cli/actions/workflows/stable.yml/badge.svg)](https://github.com/photo-cli/photo-cli/actions/workflows/stable.yml)

[![Docs](https://img.shields.io/badge/docs-photocli.com-red)](https://photocli.com) [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=photo-cli_photo-cli&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=photo-cli_photo-cli) [![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=photo-cli_photo-cli&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=photo-cli_photo-cli) [![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=photo-cli_photo-cli&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=photo-cli_photo-cli) [![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=photo-cli_photo-cli&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=photo-cli_photo-cli) [![Bugs](https://sonarcloud.io/api/project_badges/measure?project=photo-cli_photo-cli&metric=bugs)](https://sonarcloud.io/summary/new_code?id=photo-cli_photo-cli) [![GitHub license](https://img.shields.io/badge/license-Apache%202-blue.svg)](https://github.com/photo-cli/photo-cli/blob/main/LICENSE) [![Nuget pre-release](https://img.shields.io/nuget/vpre/photo-cli?label=preview&color=red)](https://www.nuget.org/packages/photo-cli/#versions-body-tab) [![.github/workflows/preview.yml](https://github.com/photo-cli/photo-cli/actions/workflows/preview.yml/badge.svg)](https://github.com/photo-cli/photo-cli/actions/workflows/preview.yml)

`photo-cli` is a [CLI](https://en.wikipedia.org/wiki/Command-line_interface) tool (works on Linux, macOS & Windows) that extracts when and where ([reverse geocode](https://en.wikipedia.org/wiki/Reverse_geocoding)) your photographs were taken, [archives](#archive) or [copies](#copy) them into a new organized folder (without modifying the source folder) with various [folder](#folder-append-type---a---folder-append-) & [file naming](#naming-style---s---naming-style-) strategies, with album support to categorize, [list & view](#list) them easily. All photo metadata is stored in a local SQLite database for archive operations and CSV for others. From the [CSV](https://en.wikipedia.org/wiki/Comma-separated_values) file (viewable in Microsoft Excel, Libre/OpenOffice Calc, Apple Numbers, Google Sheets), you can [navigate your photo locations on Google Maps & Earth with your custom label and pin style](#3-navigate-your-photo-locations-on-google-maps--earth).

## Contents

- [Features Explained With An Example](#features-explained-with-examples)
- [Installation](#installation)
- [MCP (Model Context

[...截断...]

 Protocol) Server](#mcp-model-context-protocol-server)
- [Sample Usage Screenshots](#sample-usage-screenshots)
- [How It's Done?](#how-its-done)
- [Supported Photo Types](#supported-photo-types)
- [Processing Companion Files](#processing-companion-files)
- [Address Building & Reverse Geocoding](#address-building--reverse-geocoding)
- [Usages](#usages)
- [Commands](#commands--verbs)
- [Command Line Options/Arguments](#command-line-options--arguments)
- [Settings](#settings)
- [Exit Codes](#exit-codes)
- [Contributing](#contributing)
- [Code of Conduct](#code-of-conduct)
- [Changelog - Release History](#changelog---release-history)
- [Attribution](#attribution)
- [License](#license)
- [Uninstallation](#uninstallation)
- [Credits](#credits)

## Features Explained With Examples

There are six main features that can be explained better with examples.

1. [Archive & index with albums into a specific folder with metadata stored locally on SQLite with `photo-cli archive` command](#1-archive--index-with-albums-into-a-specific-folder-with-metadata-stored-locally-on-sqlite-with-photo-cli-archive-command)
2. [Copy into a new organized folder example with `photo-cli copy` command](#2-copy-into-a-new-organized-folder-example-with-photo-cli-copy-command)
3. [List/Open Photos by their metadata on Archived Folder](#3-listopen-photos-by-their-metadata-on-archived-folder)
4. [Query your photo archive with AI assistants over MCP](#4-query-your-photo-archive-with-ai-assistants-over-mcp)
5. [Export all extracted information into a CSV Report With `photo-cli info` Command](#5-export-all-extracted-information-into-a-csv-report-with-photo-cli-info-command)
6. [Navigate Your Photo Locations on Google Maps & Earth](#6-navigate-your-photo-locations-on-google-maps--earth)

### 1. Archive & index with albums into a specific folder with metadata stored locally on SQLite with `photo-cli archive` command

#### Folder & File Hierarchy Before -> After

<table>
<tr>
    <th>Original Folder Hierarchy</th>
    <th>After <b><i>photo-cli</i></b></th>
</tr>
<tr>
<td>
<pre>
├── DSC_5727.jpg
├── GOPR6742.jpg
├── Italy album
│   ├── DJI_01732.jpg
│   ├── DJI_01733.jpg
│   ├── DSC00001.JPG
│   ├── DSC03467.jpg
│   ├── DSC_1769.JPG
│   ├── DSC_1770.JPG
│   ├── DSC_1770_(same).jpg
│   ├── DSC_1771.JPG
│   ├── GOPR7496.jpg
│   ├── GOPR7497.jpg
│   ├── IMG_0747.JPG
│   ├── IMG_1979.HEIC
│   ├── IMG_1979.mov
│   ├── IMG_1979.xmp
│   ├── IMG_2371.jpg
│   └── IMG_O1979.aae
└── Spain Journey
    ├── DSC_1807.jpg
    ├── DSC_1808.jpg
    └── IMG_5397.jpg

2 directories, 21 files
</pre>
</td>
<td>
<pre>
├── 2005
│   ├── 08
│   │   └── 13
│   │       └── 2005.08.13_09.47.23-5842c73cfdc5f347551bb6016e00c71bb1393169.jpg
│   └── 12
│       └── 14
│           └── 2005.12.14_14.39.47-03cb14d5c68beed97cbe73164de9771d537fcd96.jpg
├── 2008
│   ├── 07
│   │   └── 16
│   │       └── 2008.07.16_11.33.20-90d835861e1aa3c829e3ab28a7f01ec3a090f664.jpg
│   └── 10
│       └── 22
│           ├── 2008.10.22_16.28.39-5d66eec547469a1817bda4abe35c801359b2bb55.jpg
│           ├── 2008.10.22_16.29.49-629b0b141634d6c0906e49af448bec8d755ba32c.jpg
│           ├── 2008.10.22_16.38.20-620d23336a12ab54f9f0190fe93960a4dba2df59.jpg
│           ├── 2008.10.22_16.43.21-3b0a3215b4f66d7ff4804dd223f192c21aee71bc.jpg
│           ├── 2008.10.22_16.44.01-d470205a1d331a9d3765b3762b7c954bb8efc6ea.jpg
│           ├── 2008.10.22_16.46.53-f670f2bb6c54898894b06b083185b05086bd4e6e.jpg
│           ├── 2008.10.22_16.52.15-6b89a245809031ecc47789cdeaa332545330fc39.jpg
│           ├── 2008.10.22_16.55.37-dd42edcde2433a7df4a3d67bf61944a20884da89.jpg
│           └── 2008.10.22_17.00.07-a0ab699f5f99fce8ff49163e87c7590c2c9a66eb.jpg
├── 2012
│   └── 06
│       └── 22
│           └── 2012.06.22_19.52.31-bb649a18b3e7bb3df3701587a13f833749091817.jpg
├── 2015
│   └── 04
│       └── 10
│           ├── 2015.04.10_20.12.23-3907fc960f2873f40c8f35643dd444e0468be131.jpg
│           └── 2015.04.10_20.12.23-9f4e6d352ec172e1059571250655e376769080fe.j