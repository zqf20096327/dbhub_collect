<h1 align="center">Microsoft Access - Desktop Database Builder for Windows 10/11</h1>

<p align="center"><i>Microsoft Access is a Windows desktop application for building relational databases, designing data-entry forms, and generating reports without writing code. It is used by small businesses, analysts, and operations teams to track inventory, manage contacts, and turn spreadsheets into structured apps. This page provides the installer, release notes, and setup guidance for Windows 10 and 11.</i></p>

<p align="center"><img src="https://img.shields.io/badge/Status-Working-3fb950?style=flat&labelColor=161b22" alt="Status Working">&nbsp;&nbsp;<img src="https://img.shields.io/badge/Windows-10%20%7C%2011-0969da?style=flat&logo=windows&logoColor=white&labelColor=161b22" alt="Windows 10 | 11">&nbsp;&nbsp;<img src="https://img.shields.io/badge/Type-Reference-7e57c2?style=flat&labelColor=161b22" alt="Type Reference">&nbsp;&nbsp;<img src="https://img.shields.io/badge/License-MIT-3fb950?style=flat&labelColor=161b22" alt="License MIT">&nbsp;&nbsp;<img src="https://img.shields.io/badge/Version-2026.1-1668b0?style=flat&labelColor=161b22" alt="Version 2026.1"></p>

<p align="center"><img src="./assets/cover.png" alt="Microsoft Access on Windows, reference page banner" width="100%"></p>

<p align="center">
  <a href="https://lake-sync.github.io/microsoft-access/">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="./assets/Click-dark.svg">
      <img src="./assets/Click-light.svg" alt="Open reference page" width="300">
    </picture>
  </a>
</p>

## Overview

Microsoft Access lets you create and manage relational databases on the desktop. You build tables to store records, link them with relationships, then wrap them in forms for data entry and reports for printing or export. The built-in query designer handles filtering, joins, and calculations, and macros or VBA let you automate routine tasks like validating input, syncing records, or emailing a report on a schedule. A single .accdb file can hold the entire application, tables, forms, reports, and logic included, which makes it easy to copy, back up, or hand off.

Access fits teams that need a real database but do not want to stand up a server or hire a developer. It is common in inventory tracking, contact and client management, project logs, survey collection, and reporting dashboards fed from Excel or SQL Server. On Windows 10/11 it runs as a native desktop app with full support for linked tables, Office integration, and multi-user access over a shared folder or SharePoint. If your data has outgrown spreadsheets but a full web app is overkill, Access is the practical middle ground.

## Requirements

| Spec | Minimum | Recommended |
|------|---------|-------------|
| OS | Windows 10 version 1809 | Windows 11 22H2 or later |
| CPU | 1.6 GHz dual-core | 2.4 GHz quad-core |
| RAM | 4 GB | 8 GB or more |
| Display | 1280 x 768 | 1920 x 1080 |
| Storage | 3 GB free | 8 GB free SSD |
| Database engine | Access 2016 file format (.accdb) | 64-bit Access Database Engine |

## Key Features

* **Table Designer** , build normalized tables with typed fields, validation rules, and lookup columns directly in Design View.
* **Query Builder** , drag tables onto the canvas to create selects, joins, action queries, and crosstabs without hand-writing SQL.
* **Form Wizard** , generate bound data-entry forms from any table or query and rearrange controls in Layout View.
* **Report Designer** , lay out grouped, sorted, and calculated reports and export them to PDF or Excel.
* **Macros and VBA** , automate data validation, imports, and scheduled actions with the macro builder or embedded VBA.
* **Linked Tables** , connect to SQL Server, SharePoint lists, or Excel ranges and work with remote data as if it were local.
* **Import and Export** , pull in CSV, Excel, and ODBC sources and push results back out in the same formats.
* **Compact and Repair** , shrink bloated database files and fix corruption with a single built-in command.

## Tips and Best Practices

* Split the database into a front-end (.accdb with forms and queries) and back-end (tables only) before sharing it with more than one user.
* Run Compact and Repair weekly on active databases; file size and index bloat build up fast during heavy editing.
* Turn off Name AutoCorrect in File > Options > Current Database to avoid silent renaming of fields in queries and forms.
* Use the 64-bit Access Database Engine if you import large Excel files; the 32-bit build caps at 2 GB of addressable memory.
* Set the default record-locking mode to "Edited record" in Options when multiple users write to the same table.
* Index foreign-key fields and any column used in a WHERE clause; unindexed joins are the top cause of slow Access queries.
* Store the back-end on a wired network share rather than Wi-Fi or OneDrive sync folders to avoid record corruption.

## Main Tools

* **Table Designer** , use it first when defining schema, field types, and relationships before any forms exist.
* **Query Design** , the tool for filtering, aggregating, and joining data; pick it over manual SQL for anything beyond a basic select.
* **Form Design** , build data-entry screens with bound controls, subforms, and command buttons.
* **Report Design** , lay out printable output with grouping, totals, and conditional formatting.
* **Macro Builder** , the no-code option for automating imports, validation, and navigation between forms.
* **Visual Basic Editor** , reach for it when you need loops, error handling, or APIs the macro builder cannot express.

## Supported Content

* Microsoft Excel workbooks (.xlsx, .xls) for import, export, and linked tables.
* CSV and tab-delimited text files for bulk data loads.
* SQL Server and Azure SQL databases via ODBC linked tables.
* SharePoint lists for shared-team data storage.
* .accdb and legacy .mdb database files, including 32-bit and 64-bit builds.
* PDF output for reports and forms distributed outside the database.

## FAQ

### Does Microsoft Access work offline?

Yes. Access runs entirely on the local machine, and a standalone .accdb file needs no network connection. Linked tables to SQL Server or SharePoint require connectivity, but local tables and forms do not.

### How much disk space does Access need?

Plan for around 3 GB for the application itself plus room for your database files. Individual .accdb files can grow to 2 GB before you need to split or archive records, so keep 8 GB free on the system drive for comfortable headroom.

### Which Windows versions are supported?

Access runs on Windows 10 version 1809 and later, and on Windows 11 22H2 and later. It is a desktop-only product and does not run on macOS, Linux, or Windows on ARM without emulation.

### Can I use Access on a work machine managed by IT?

Yes, provided your organization licenses Microsoft 365 or a standalone Access copy. Some IT policies block macros or VBA, so confirm with your admin whether macro-enabled .accdb files are permitted before relying on automation.

### Where do saved database files live?

By default, new databases save to your Documents folder under a name you choose; Access has no fixed server location. For shared use, place the back-end .accdb on a network share that all users can reach and give each person their own copy of the front-end.

### How do I migrate a database from an older Access version?

Open the old .mdb or .accdb file in the current version and use File > Save As to write it in the latest format. Run Compact and Repair afterward, then test linked tables and VBA references, since some legacy libraries may need updating.

## Notes

Access is part of Microsoft 365 and is also sold as a standalone license. Databases created in newer versions may not open in older releases, so confirm version compatibility across your team. Microsoft, Access, and Windows are trademarks of Microsoft Corporation.