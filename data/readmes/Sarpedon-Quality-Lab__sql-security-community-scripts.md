# Get-SqlSafe: Free SQL Server Security Check and Assessment Script (Community Edition)

**By [Andreas Wolter](https://andreas-wolter.com/en/), former Microsoft Senior Program Manager for SQL Server security and one of 7 Microsoft Certified Solutions Masters (MCSM): Data Platform. [Sarpedon Quality Lab](https://sarpedonqualitylab.us/).**
Version 2026.7

Get-SqlSafe Community Edition is a free SQL Server security check: a standalone PowerShell script that runs 27 core checks and writes a local HTML report for review and remediation discussions. It is read-only: it does not modify SQL Server or database configuration or user data. It works with SQL Server, SQL Server on Amazon RDS and Azure SQL Database.

The Community Edition is designed as a practical first look at SQL Server security posture. It focuses on baseline indicators such as authentication exposure, auditing gaps, excessive privileges, risky configuration settings, orphaned or dependent accounts, and database ownership drift.

> **Note:** This tool identifies indicators of risk. It is not a full security audit, penetration test, compliance assessment, or guarantee of security.

Need more than a first look? The full [Sarpedon SQL Server Security Assessment](https://sarpedonqualitylab.us/sql-server-security-assessment/) covers about 90 to more than 140 checks, reviewed by a former Microsoft Senior Program Manager for SQL Server security.

Overview, FAQ and what the full assessment adds: [Free SQL Server Security Check (Get-SqlSafe)](https://sarpedonqualitylab.us/free-sql-server-security-check/).

Read the [original public introduction to Get-SqlSafe Community Edition](https://andreas-wolter.com/en/2605_get-sqlsafe_communityedition_sqlserver_security_asssessment_tool/).

![Get-SqlSafe 2026.7 report header with a report note and the Outcome Summary tiles](images/report-summary.png)

## Trust at a Glance

Get-SqlSafe Community Edition is built to be reviewed before it is run. For SQL Server and Amazon RDS:

- **Plain-text PowerShell.** One readable `.ps1` script with embedded, inspectable T-SQL. No compiled binaries, no DLLs, no obfuscated or encoded payloads.
- **No PowerShell module imports.** SQL Server and Amazon RDS use the built-in .NET `System.Data.SqlClient` only. No modules are loaded or installed. (Azure SQL Database is the one exception and uses Microsoft's own `SqlServer` / `Az.Accounts` modules, which you install yourself.)
- **Read-only.** The assessment queries security metadata. It does not change SQL Server configuration, database settings, or user data.
- **No outbound calls except the target.** The script connects only to the SQL Server, RDS, or Azure SQL instance you point it at (plus Microsoft's sign-in service when you choose Azure Microsoft Entra authentication). It contains no web requests, update checks, telemetry, or analytics.
- **No registration.** Download and run. Nothing to sign up for, no license key, no activation.
- **Self-contained report.** The generated HTML is a single local file with inline styles and script, a logo embedded as data, and system fonts. It loads no external scripts, fonts, images, stylesheets, or trackers. The only outbound references are documentation hyperlinks you choose to click.
- **Writes only under `Results`.** Reports and optional logs are written to the `Results` folder next to the script, and nowhere else. (See the note on the alternate-Windows-account option under Enterprise Usage and Trust.)
- **Integrity checks built in.** The embedded T-SQL is verified against a stored SHA-256 hash before it runs, and each release publishes the file hashes so you can confirm the download.


---

## What This Tool Does

`Get-SqlSafe.ps1` is a simple, reviewable PowerShell script that helps identify high-level SQL Server security posture indicators. It focuses on common security-relevant areas such as authentication, privileged access, server-level permissions, risky configuration, audit visibility, ownership risks, and orphaned accounts.

This Community Edition is designed to:

- Operate under least-privilege principles where supported by the target SQL Server version.
- Output a clean, visual local HTML report.
- Be transparent and easy to review as plain-text PowerShell with embedded T-SQL.
- Avoid automatic dependency installation.
- Run SQL Server and Amazon RDS assessments without external PowerShell modules. Azure SQL Database uses one optional module and separately installed Microsoft prerequisites.
- Support both GUI-based and console-based execution.
- Support selected checks against SQL Server on Amazon RDS through an explicit compatibility mode, and Azure SQL Database through an optional component.


---

## What Changed in 2026.7

Version 2026.7 builds on the previous public release, 2026.6.

- Replaced the 2026.6 securityadmin-based permission setup with two SQL Server profiles: a full assessment with **sysadmin**, or a limited profile with read grants only that skips checks `046`, `050`, `069` and `072`. See [Required SQL Server Permissions](#required-sql-server-permissions).
- Redesigned the HTML report for a management audience: an Outcome Summary with one tile per outcome and a headline such as "14 of 25 core security controls need action", worst-first ordering throughout, linked categories, lighter check rows and a closing scope statement that names the platform the report was run against.
- Hardened the alternate Windows account option: no temporary files, a plain `-File` relaunch instead of an encoded command, `RemoteSigned` instead of `Bypass`, and a visible window.
- Added an optional one-line **report note** (`-ReportNote`, or the Report options area of the dialog). The note is limited to 150 Unicode code points, supports `**bold**`, is HTML-escaped, and records the invoking Windows account automatically. It is a presentation note, not a finding exception.
- Added explicit Azure sign-in controls: `-AzureUseDeviceAuthentication` for device-code sign-in and optional `-AzureTenantId`. Browser sign-in remains the default.
- Reorganized the connection dialog into Connection settings and a separate Report options area.
- Added distinct exit codes so wrappers can tell failures apart: `3` SQL execution failure, `4` publication failure, `5` both.
- Made report publication atomic: required HTML files are written through temporary files and verified before a run is reported as successful. Report filenames use readable server/database names and minute timestamps, with numeric suffixes when filenames collide.
- Hardened evidence handling across many checks so hidden or unavailable metadata no longer produces a false `PASS`, with correctness fixes to checks including `050`, `059`, `069`, `129`, `155`, and the database-owner checks.

See [CHANGELOG.md](CHANGELOG.md) for the full 2026.7 detail and the preserved history of earlier public releases.

## Earlier Releases

2026.6 added Azure SQL Database (Microsoft Entra and SQL authentication) with the optional `Get-SqlSafe.Azure.psm1` module, the SQL Server / AWS RDS / Azure target selectors, and Check `030` for instance-wide cross-database ownership chaining. 2026.5 introduced individual database reports and Check `130` for `db_owner` role members. 2026.4 added AWS RDS compatibility. Their history is retained in [CHANGELOG.md](CHANGELOG.md).

## Contents

There is one 2026.7 download, `Get-SqlSafe.zip`, containing:

```text
Get-SqlSafe.ps1
Get-SqlSafe.Azure.psm1
README.md
CHANGELOG.md
LICENSE.md
```

`Get-SqlSafe.ps1` is the same script for all targets. SQL Server and Amazon RDS users can omit or delete `Get-SqlSafe.Azure.psm1`. They do not need the Microsoft Azure prerequisites.

Only Azure SQL Database needs the optional module beside the script and the Microsoft modules listed below. The optional module is plain PowerShell code, with no bundled DLLs, separate SQL file or Get-SqlSafe dependency cache. If it is missing when Azure is selected, the script reports the missing optional component. Reports and optional logs are written beneath `Results` next to the script. Keep the script and optional module from the same release together.

## Requirements

- Windows PowerShell 5.1 on Windows.
- Network access to the database target and permissions to read the assessed metadata.
- SQL Server 2016 or newer is recommended for SQL Server/RDS. SQL Server 2012 and 2014 may require broader permissions for selected checks.
- SQL Server and Amazon RDS use .NET `System.Data.SqlClient` and require no external PowerShell modules.
- Azure SQL Database requires .NET Framework 4.7.2 or later and the Microsoft `SqlServer` module, version 22.4.5.1 or later. Microsoft Entra authentication additionally requires `Az.Accounts`, version 5.3.4 or later.

Install the Azure prerequisites once as the account that runs the assessment:

```powershell
Install-Module SqlServer -MinimumVersion 22.4.5.1 -Scope CurrentUser
Install-Module Az.Accounts -MinimumVersion 5.3.4 -Scope CurrentUser
```

Use `-RequiredVersion` instead of `-MinimumVersion` to install those exact versions. For Azure SQL Database, SQL authentication requires the Microsoft `SqlServer` module but not `Az.Accounts`. The collector never installs or updates modules automatically. An administrator can provision them offline where PowerShell Gallery access is restricted.

Neither Microsoft module is imported for SQL Server or Amazon RDS. For Azure, the optional component uses the driver supplied by `SqlServer`; `Az.Accounts` handles browser-based sign-in/MFA and SQL access tokens. Microsoft modules maintain their own dependencies and authentication state. No Get-SqlSafe-specific library download, cache or compiled helper is used.

## Supported Targets and Known Limitations

Supported targets are SQL Server on-premises or in a virtual machine, SQL Server on Amazon RDS, and Azure SQL Database. Azure SQL Managed Instance is not an Azure SQL Database target in this release.

Use Windows or SQL authentication for SQL Server/RDS. Use SQL authentication or Microsoft Entra Interactive for Azure SQL Database. Azure Entra sign-in opens the system browser and supports MFA. Complete sign-in in the browser, then return to PowerShell.

For RDS, select AWS RDS in the dialog or supply `-Platform AwsRds`. For Azure, use the optional module and select Azure SQL Database or supply `-Platform AzureSQLDatabase`.
In GUI mode, Azure SQL Database assessments target databases discoverable through `master` by the connected identity. Console mode defaults to `master` when neither `-AzureDatabase` nor `-AzureAllVisibleDatabases` is specified, and also supports an explicit database. A visible database inventory is not a guarantee that every database on the logical server is listed or accessible.

Some SQL Server checks do not apply to Azure SQL Database and are omitted entirely. Other Azure entries describe service-managed behavior or settings outside SQL metadata visibility. Checks `003`, `004` and `015` are not executed when the indirect administrator-visibility probe is negative or unavailable. The probe does not deterministically establish Server admin or Microsoft Entra administrator status. Verify administrator status and service-level configuration through the Azure control plane; the collector does not read that configuration.

On SQL Server/RDS, authentication-scheme metadata can be misleading for Microsoft Entra-authenticated sessions. Azure SQL Database support does not extend Microsoft Entra authentication support to SQL Server instances or Azure SQL Managed Instance.

Contained availability group metadata requires the relevant SQL Server catalog views. Checks affected by a contained availability group's separate security context may require assessment through that connection context.

## Quick Start - GUI Mode

1. Extract the selected package and open Windows PowerShell. For Azure, install the prerequisites listed above.
2. If required by your organization's download-handling process, unblock the files:

   ```powershell
   Unblock-File .\Get-SqlSafe.ps1
   # Only when using Azure SQL Database:
   Unblock-File .\Get-SqlSafe.Azure.psm1
   ```

3. Run the script:

   ```powershell
   .\Get-SqlSafe.ps1
   ```

4. Select SQL Server, AWS RDS or Azure SQL Database and enter the server name.
5. Choose an authentication method supported by that target. Azure Entra sign-in uses the browser when a connection is opened.
6. Review Connection settings and Limited-access options. Skip checks requiring sysadmin applies only to SQL Server and skips 046, 050, 069 and 072. The separate Azure option skips 003, 004 and 015.
7. Optionally request per-database reports or use Test Connection and Permissions. On Azure, the permission test adapts its required access rows to the active checks.
8. Start the assessment.

The HTML report opens automatically unless `-NoAutoOpenReport` is supplied. Azure does not show an additional completion popup after writing the report. A failed authentication or assessment still reports the failure.

## Quick Start - Console Mode

Supplying `-SqlInstance` automatically runs the script in console mode.

Windows authentication:

```powershell
.\Get-SqlSafe.ps1 -SqlInstance "SQLPROD01"
```

Run without opening the report automatically:

```powershell
.\Get-SqlSafe.ps1 -SqlInstance "SQLPROD01" -NoAutoOpenReport
```

SQL authentication:

```powershell
$sqlPassword = Read-Host "SQL password" -AsSecureString
.\Get-SqlSafe.ps1 -SqlInstance "SQLPROD01" -Auth SQL -SqlUser "assessment_user" -SqlPass $sqlPassword -NoAutoOpenReport
```

Mandatory encryption while trusting the server certificate:

```powershell
.\Get-SqlSafe.ps1 -SqlInstance "SQLPROD01" -Encrypt Mandatory -TrustServerCert -NoAutoOpenReport
```

AWS RDS compatibility mode:

```powershell
.\Get-SqlSafe.ps1 -SqlInstance "my-rds-instance.example.rds.amazonaws.com" -Platform AwsRds -Encrypt Mandatory -TrustServerCert
```

Write a run log:

```powershell
.\Get-SqlSafe.ps1 -SqlInstance "SQLPROD01" -WriteLog -Verbose -NoAutoOpenReport
```

Console mode and `-NoAutoOpenReport` are useful for controlled endpoints, automation-friendly execution, and EDR/XDR-controlled environments where UI prompts or automatic browser launches may be restricted.

---

### Azure SQL Database with Microsoft Entra Interactive

```powershell
.\Get-SqlSafe.ps1 -Platform AzureSQLDatabase -Auth EntraInteractive -SqlInstance 'contoso.database.windows.net' -AzureAllVisibleDatabases -NoAutoOpenReport
```

For a single database, replace `-AzureAllVisibleDatabases` with `-AzureDatabase 'appdb'`. Entra authentication remains interactive even in console mode, so complete the browser sign-in/MFA.

### Azure SQL Database with SQL Authentication

```powershell
$password = Read-Host 'Azure SQL password' -AsSecureString
.\Get-SqlSafe.ps1 -Platform AzureSQLDatabase -Auth SQL -SqlUser 'SecurityAssessment' -SqlPass $password -SqlInstance 'contoso.database.windows.net' -AzureDatabase 'appdb' -NoAutoOpenReport
```

Azure connections always enforce `Encrypt=Strict` with certificate validation, regardless of the non-Azure default encryption setting. `-TrustServerCert` cannot weaken the Azure connection.

## Parameters

| Parameter | Purpose |
| --- | --- |
| `-SqlInstance` | Target SQL Server instance or Azure SQL logical server. Supplying it enables console mode. |
| `-ConsoleOnly` | Runs without the WPF dialog. Aliases: `-NoUI`, `-NonInteractive`. Entra sign-in still requires interaction. |
| `-Platform` | `SQLServer` (default), `AwsRds`, or `AzureSQLDatabase`. |
| `-Auth` | `Windows` (default for SQL Server/RDS), `SQL`, or `EntraInteractive` (default for Azure SQL Database). EntraInteractive requires Azure SQL Database. |
| `-SqlUser` | SQL login name, required for SQL authentication. |
| `-SqlPass` | SQL login password as a SecureString. SQL Server/RDS prompts if omitted. Azure SQL authentication requires an explicit `-SqlPass`; omission stops execution. |
| `-AzureDatabase` | Azure SQL Database to assess. Defaults to `master` when `-AzureAllVisibleDatabases` is not selected. |
| `-AzureAllVisibleDatabases` | Assess the Azure databases visible to this identity in master. Do not combine with `-AzureDatabase`. |
| `-AzureUseDeviceAuthentication` | Use Microsoft device-code sign-in for Azure SQL Database instead of browser sign-in. Microsoft Entra authentication only. |
| `-AzureTenantId` | Optional Microsoft Entra tenant ID for Azure SQL Database sign-in. |
| `-Encrypt` | `Optional`, `Mandatory` or `Strict`. Optional is the SQL Server/RDS default; Azure always enforces Strict. Strict requires Azure. |
| `-TrustServerCert` | SQL Server/RDS certificate-trust option. Azure always validates its certificate. |
| `-SkipChecks` | Explicit check IDs to skip, such as `-SkipChecks 046,050,069,072` or Azure `-SkipChecks 003,004,015`. Skipped entries are shown as Not checked. |
| `-CreateIndividualDBLevelReports` | Additionally write reports containing database-scoped checks for individual databases. |
| `-ReportNote` | Optional one-line note in the report header, up to 150 characters including `**` markers. `**text**` is shown in bold. The Windows account that ran the assessment is added automatically. |
| `-AwsRdsCompat` | Backwards compatibility only: Use -Platform AwsRds instead. Enable AWS RDS compatibility behavior and AWS managed labels. |
| `-WindowsCredential` | Relaunch under another Windows account. Requires Windows authentication and `-SqlInstance`. |
| `-WriteLog` | Write a run log under Results. Alias: `-LogFile`. |
| `-Verbose` | Show verbose progress independently of file logging. |
| `-NoAutoOpenReport` | Write reports without launching the browser to display them. |

Use `Get-Help .\Get-SqlSafe.ps1 -Full` for script help. The Azure component contains the Azure-specific queries and connection handling.

## Connection Encryption

For SQL Server and Amazon RDS, `-Encrypt` and `-TrustServerCert` work together:

| Encryption | Trust certificate | Result |
| --- | --- | --- |
| `Optional` (default) | off or on | No practical difference. The certificate is not validated either way. |
| `Mandatory` | off | The session is encrypted and the certificate is validated: the chain must be trusted, the certificate unexpired, and its name must match the server name as typed. A stock instance using its auto-generated self-signed certificate will fail this. |
| `Mandatory` | on | The session is encrypted, but any certificate is accepted. This protects against passive interception, not against an active man-in-the-middle. |

The login packet, including the password when `-Auth SQL` is used, is encrypted during the TDS pre-login handshake regardless of these settings. `Optional` means the rest of the session - the queries and all result rows - is unencrypted and no certificate is verified.

One exception to the first row: if the instance has `ForceEncryption` enabled, the server imposes encryption even when `Optional` was requested, and certificate validation then applies. That is the usual reason an `Optional` connection unexpectedly fails on certificate trust.

For an assessment run across an untrusted network, prefer `-Encrypt Mandatory` with a properly issued certificate and without `-TrustServerCert`.

---

Azure SQL Database always uses Strict encryption with certificate validation. Its connection ignores the non-Azure Optional default and does not permit TrustServerCertificate to weaken validation.

## Authentication Modes

### Windows Authentication

Use Windows authentication when the current Windows account has the required SQL Server permissions:

```powershell
.\Get-SqlSafe.ps1 -SqlInstance "SQLPROD01"
```

### Alternate Windows Account

Use `-WindowsCredential` to relaunch the assessment under another Windows identity:

```powershell
$cred = Get-Credential
.\Get-SqlSafe.ps1 -ConsoleOnly -SqlInstance "SQLPROD01" -Auth Windows -WindowsCredential $cred -NoAutoOpenReport
```

### SQL Authentication

Use SQL authentication with a secure password prompt:

```powershell
$sqlPassword = Read-Host "SQL password" -AsSecureString
.\Get-SqlSafe.ps1 -SqlInstance "SQLPROD01" -Auth SQL -SqlUser "assessment_user" -SqlPass $sqlPassword
```

---

## AWS RDS Compatibility Mode

Use `-Platform AwsRds` when assessing SQL Server on Amazon RDS.

When enabled, the collector:

- Adjusts selected permission checks for restricted AWS-managed environments.
- Skips Check `046` because the required server-level access is not normally available on SQL Server on Amazon RDS.
- Excludes AWS-managed objects such as `rdsadmin` where applicable.
- Excludes the `model` database from selected owner checks.
- Marks selected findings with an `AWS managed` label when the target is detected as RDS.

AWS RDS compatibility mode does not imply that every control managed by AWS is secure or correctly configured. It distinguishes selected platform-managed conditions from findings under direct customer control.

---

## Contained Availability Groups

Check `802` reports contained availability group names and listener DNS/port details when SQL Server 2022 or newer exposes the required metadata.

> **Important:** Contained availability groups maintain security principals and metadata separately from the host SQL Server instance. Checks that depend on this security context, such as identifying orphaned database users, must be executed through the contained availability group context to produce accurate results.

---

## User-database ownership checks

Checks `072` (User Database Owner sysadmin) and `078` (User Database Owner Windows Account) assess online user databases only. `master`, `model`, `msdb` and `tempdb` do not produce owner results or PASS entries. Check `010` remains the separate direct individual-sysadmin-grant check. A system-database-owner-change rule is deferred.

Check `072` reports OBSERVE when effective sysadmin membership is proven by direct/nested SQL role paths or Windows permission-path evidence. PASS requires sufficient complete evidence of nonmembership. Insufficient resolution remains unevaluated, with a safe reason and incomplete coverage. When selected without sysadmin, it is Not assessed. A failed supplementary lookup does not remove a proven finding. Check `078` independently reports WARNING for a known Windows user/group owner, including when `072` is inconclusive; its recommendation concerns user-database ownership portability and account availability.

For a full self-managed SQL Server assessment, use a sysadmin account. This supported profile applies to checks `046`, `050`, `069` and `072`, including registry and Windows-owner operations. The limited profile skips those four checks. Check `078` remains assessable from visible owner metadata when `072` is skipped or cannot run. SQL Server 2022 security-definition visibility accepts `VIEW ANY SECURITY DEFINITION`, including covering grants; earlier versions use `VIEW ANY DEFINITION`.

The collector uses owner-specific `xp_logininfo` calls with `all` and caches distinct owner/group lookups only while eligible check `072` runs. The assessment grants no permissions. Skipping or lacking eligibility for `072` prevents those auxiliary calls.

Microsoft documents that `xp_logininfo` does not cover Active Directory universal groups. Therefore successful non-admin output alone cannot establish complete domain-owner nonmembership. Positive evidence is retained; unsupported domain/group resolution remains Not evaluated. Fully resolved supported local-account paths can establish nonmembership when server-role metadata is also complete. See [Microsoft's xp_logininfo documentation](https://learn.microsoft.com/en-us/sql/relational-databases/system-stored-procedures/xp-logininfo-transact-sql).

## Dialog options and report note

![Connection dialog with the target selector, the Connection settings, Limited-access options and Report options panels, and a report note](images/gui-connection-dialog.png)

Connection settings, Limited-access options and Report options share one row. Opening one panel closes the others; all may be collapsed, and entered values are preserved. Limited-access options contains Skip checks requiring sysadmin (SQL Server only: 046, 050, 069, 072) and the separate Azure administrator skip option (003, 004, 015). The sysadmin option is disabled and ignored on AWS RDS and Azure SQL Database. Explicit -SkipChecks selections are preserved when controls or platforms change.

The note field accepts at most 150 Unicode code points, including spaces and `**` markers. Typing past the limit is blocked. Paste accepts only the part that fits, including when replacing a selection. Supplementary Unicode characters count once and are not split. Console input exceeding the limit is rejected by the existing validator.


## Required SQL Server Permissions

A full self-managed SQL Server assessment requires **sysadmin**. The connection/permission test shows the connected login, engine version, effective sysadmin membership and a concise result. Membership in securityadmin or CONTROL SERVER without sysadmin does not establish this supported full profile.

For a supported limited assessment, use a dedicated login and select **Skip checks requiring sysadmin**, or run:

```powershell
.\Get-SqlSafe.ps1 -SqlInstance 'SQLPROD01' -SkipChecks 046,050,069,072
```

The checkbox adds those four exclusions while retaining explicit CLI skips. Unchecking it removes only the checkbox's additions. Selected administrative checks without sysadmin are Not assessed, with a missing-role reason; independent checks continue. Explicit exclusions are Not checked. Coverage gaps remain in the report and execution log/run state. Neither state is counted in assessed header totals, outcome graphics, tiles or percentage denominators. Proven partial findings remain visible and counted.

### SQL Server 2022 and later limited profile

Have an administrator grant the following to the existing assessment login:

```sql
USE master;
GRANT VIEW ANY SECURITY DEFINITION TO [SqlAssessmentReader];
GRANT VIEW SERVER SECURITY STATE TO [SqlAssessmentReader];
GRANT VIEW SERVER PERFORMANCE STATE TO [SqlAssessmentReader];
GRANT VIEW ANY DATABASE TO [SqlAssessmentReader];
GRANT CONNECT ANY DATABASE TO [SqlAssessmentReader];
```

The test accepts effective, inherited and covering grants. VIEW ANY DEFINITION covers security-definition access; VIEW SERVER STATE covers both state permissions. CONNECT ANY DATABASE is mandatory for this supported limited profile. Database-specific CONNECT grants are not a preflight substitute, and the permission test performs no extra user-database connection probes. Ordinary database connections and visibility checks still occur during collection; database DENY permissions or other restrictions can leave individual checks incomplete.

### SQL Server 2014-2019 limited profile

```sql
USE master;
GRANT VIEW ANY DEFINITION TO [SqlAssessmentReader];
GRANT VIEW SERVER STATE TO [SqlAssessmentReader];
GRANT VIEW ANY DATABASE TO [SqlAssessmentReader];
GRANT CONNECT ANY DATABASE TO [SqlAssessmentReader];
```

Use the same four-check skip list. The permission message uses this version's permission names.

### SQL Server 2012

SQL Server 2012 does not provide CONNECT ANY DATABASE or the SQL Server 2022 granular permissions. Its limited-profile permission test checks VIEW ANY DEFINITION, VIEW SERVER STATE and VIEW ANY DATABASE only. It does not display a fabricated CONNECT ANY DATABASE result or run user-database preflight connections. Collection still requires actual database access and qualifies missing evidence. The live limited-profile matrix was established on SQL Server 2022; older-engine execution requires separate verification.

### Amazon RDS for SQL Server

Use `-Platform AwsRds` and an account with the metadata/state access available under the RDS model. The self-managed sysadmin checkbox is disabled and ignored. RDS still forces the existing 046 exclusion and retains its own eligibility for supported registry/owner operations. Explicit CLI skips remain available. The script never elevates the assessment account or provisions permissions.

## Azure SQL Database Permissions

Use an existing SQL server administrator, Microsoft Entra administrator, or an assessment login with this three-role grant profile in logical master:

```sql
ALTER SERVER ROLE ##MS_DatabaseConnector## ADD MEMBER [SecurityAssessment];
ALTER SERVER ROLE ##MS_SecurityDefinitionReader## ADD MEMBER [SecurityAssessment];
ALTER SERVER ROLE ##MS_ServerStateReader## ADD MEMBER [SecurityAssessment];
```

The permission test connects to master and checks effective access under that authenticated session. It displays role-access labels, not literal membership assertions. Administrator access, covering permissions and access inherited through Entra groups can satisfy the checks without direct membership rows for the individual user. The labels describe access needed by the selected operations normally supplied by those roles; they do not assert that every role permission was tested or that individual database DENY overrides are absent.

Requirements and displayed rows follow active checks. Skipping 003, 004 and 015 removes their state requirement when no remaining check needs it; active 113/130 still require database security metadata access. A confirmed absence displays No. Inconclusive access displays Unknown and fails the permission test. Collection still connects independently to selected databases and records missing access or metadata evidence.

The permission message always states: **Microsoft Entra administrator status cannot be determined reliably from this test.**

---

## Checks and Report Content

On SQL Server, Get-SqlSafe runs 31 checks: 27 core security controls and 4 informational items. The limited permission profile skips 4 of the core controls (`046`, `050`, `069`, `072`), so 23 run. Amazon RDS and Azure SQL Database run fewer, because some checks do not apply there. A report scores only the controls it could assess: skipped and not assessed checks are listed, but not counted, so a report can show fewer than 27.

### Common questions it answers

| Question | Check |
|---|---|
| Who is a member of the sysadmin role? | `010` Sysadmin members, individual accounts |
| Is `xp_cmdshell` enabled? | `034` xp_cmdshell setting |
| Are there orphaned database users? | `129` Orphaned database users |
| Are there orphaned Windows logins? | `046` Orphaned Windows logins |
| Is the `sa` login renamed and disabled? | `008` SA login name, `079` SA login state |
| Which databases have `TRUSTWORTHY` set? | `028` Databases with TRUSTWORTHY |
| Which SQL logins skip the password policy? | `006` SQL logins without password policy enforcement |
| Is SQL authentication or NTLM still in use? | `003` SQL authentication usage, `004` NTLM authentication usage |
| Who is `db_owner` in each database? | `130` db_owner database role members |
| Are failed logins logged, and is SQL Server Audit set up? | `069` Login failure logging, `059` SQL Server Audit minimal setup |

### All areas covered

- Authentication configuration
- SQL authentication, password-policy enforcement, and NTLM usage
- Sysadmin and powerful server role memberships
- Server-level permissions
- `TRUSTWORTHY` and cross-database ownership chaining
- Powerful features such as `xp_cmdshell`, ad hoc distributed queries, and OLE Automation
- Orphaned Windows logins and database users
- `db_owner` database role membership
- SQL Server Audit configuration
- Database ownership risks
- SQL Server error log retention
- Availability groups and contained availability groups
- System overview and informational context

The HTML report includes:

- Header with target server, report date, and the number of core security controls, informational items and sections
- Optional report note with the Windows account that added it
- Outcome Summary: one tile per outcome, a stacked bar of the core security controls and a headline such as "14 of 25 core security controls need action"
- Outcome filters showing the number of results per outcome
- Category summary table with counts per outcome and a total; category names link to their sections
- Outcome definition legend
- Detailed findings grouped by category
- Recommendations and references for actionable findings
- Informational context for version and system overview checks
- A closing Scope and limitations panel that names the platform assessed and the number of controls covered

![Check rows grouped by category, each with its outcome badge and a colored left edge](images/report-check-rows.png)

When per-database reports are requested, each database additionally receives its own report containing the database-scoped checks for that database, with the same Outcome Summary.

---

## Result Meanings

The report uses five outcome states, plus two grey states that are not scored: Not checked and Not assessed.

| Outcome | Meaning |
| --- | --- |
| `INFO` | Provides useful context. It does not indicate a security finding. |
| `PASS` | The assessed condition met the expected rule. |
| `OBSERVE` | Marks a condition that is not necessarily risky by itself but should be reviewed or monitored. Impact depends on environment, intent, and compensating controls. |
| `WARNING` | Indicates a security-relevant finding that should be reviewed and usually remediated, but does not by itself indicate immediate high risk. |
| `FAIL` | Indicates a clear security risk that requires prompt attention. |
| `Not checked` | The included check was skipped. Grey, with no PASS/failure assignment or expandable findings. |
| `Not assessed` | The check could not be evaluated, for example because of missing permissions, hidden metadata or too few connections. Grey and not scored. |

For `OBSERVE`, `WARNING`, and `FAIL` findings, the report includes recommendation text and, where available, reference links.

---


A query failure or missing evidence is not a PASS. Azure reports may indicate that a check was not assessed or only partially assessed when required evidence is unavailable. Successful PASS entries show only the heading and outcome, with no empty results panel.

Check `003` needs at least ten eligible workload connections; smaller samples are Not assessed. For Check `004`, fewer than ten eligible connections produces WARNING on SQL Server/RDS and OBSERVE on Azure, with only the recommendation to repeat the scan during representative activity. With at least ten connections, SQL Server/RDS uses the NTLM percentage rules and Kerberos guidance. Azure uses Entra guidance and changes the SQL Server FAIL outcome to OBSERVE because visible NTLM connections can be associated with Azure services and features. Connection samples reflect observed metadata, not guaranteed complete server coverage.

Outcomes with a count of zero are left out of the stacked bar. Print output includes collapsed evidence and recommendations; Expand All and Collapse All operate on the currently visible expandable sections.

## Output, Security, and Data Handling

The tool generates a local HTML report in the `Results` folder. All report filenames follow `<server>[_DB_<database>]_Get-SqlSafe_<yyyyMMdd_HHmm>.html`. The database portion appears only in individual database reports. Timestamps use local time to the minute. Filename collisions receive `_2`, `_3`, and so on after the timestamp. Invalid filename characters are replaced and long names are shortened to fit the supported Windows path budget. When `-WriteLog` is used, a `.log` file with the same basename as the main report is written to that folder. Local aliases such as `.\Sql2019` use the local machine name; named instances use `$` in filenames.

With `-CreateIndividualDBLevelReports`, the per-database reports are written to a `<ServerName>__<Timestamp>__DatabaseLevelReports` sub-folder inside `Results`, and the main report links to that folder. These reports contain the same findings as the main report, scoped to a single database.

Generated reports and logs may include sensitive environment-specific information, including:

- Server and database names
- Login and role membership details
- Permission details
- Configuration values
- Database ownership details
- Security findings and recommendations

Handle generated reports according to your organization's data handling and confidentiality requirements.

The assessment does not modify SQL Server or database configuration or user data. Azure Entra authentication selects browser login only for the current PowerShell process. It reads metadata and reports high-level indicators.

---

## SQL Integrity Validation

The embedded SQL assessment text is validated before execution using SHA-256.

The required hash is stored in the script and compared against the embedded SQL text before execution. If the embedded SQL text does not match the required hash, execution stops.

This helps detect accidental edits, copy/paste damage, or mismatched build artifacts. For enterprise tamper protection, use your normal file-hash validation and code-signing process.

The required hash changes whenever the embedded SQL text changes, including its version banner, so it differs between releases.

---

## Exit Codes

```text
0 = completed successfully
2 = startup, parameter, credential, assessment source validation failure, or some Azure connection/authentication exceptions
3 = SQL connection or execution failure, including Azure assessments that produce no publishable report
4 = a required report file could not be written
5 = SQL execution failure and a required report file could not be written
```

---

## Enterprise Usage and Trust

This tool is distributed as a plain-text PowerShell script so organizations can review it according to internal security and change-control processes.

### Behavior Summary

Get-SqlSafe Community Edition:

- Runs locally from the extracted folder.
- Connects to SQL Server/RDS using Windows or SQL authentication, or Azure SQL Database using SQL authentication or browser-based Microsoft Entra authentication.
- Executes embedded SQL assessment logic.
- Validates the embedded SQL text using SHA-256 before execution.
- Writes a local HTML report to the `Results` folder, and nothing outside it.
- Can optionally write a run log to the `Results` folder.
- Does not install PowerShell modules automatically.
- Does not modify SQL Server or database configuration or user data.
- Makes no outbound network connection other than to the assessed database instance (and, for Azure Microsoft Entra authentication, Microsoft's sign-in service).

#### Note on the alternate-Windows-account option

When you supply `-WindowsCredential` (console mode only), the script runs the assessment under that Windows account. Because a different account cannot share the current session, the script starts one child PowerShell process as that account with `Start-Process`, using the standard `-File` invocation under the `RemoteSigned` execution policy, waits for it, and returns its exit code. The report note text and author name, if a note is used, are passed to that child as ordinary command-line parameters. No SQL password is ever passed this way, because this option supports Windows authentication only, and nothing is written outside the `Results` folder. A reviewer reading the code will find this relaunch path in the `-WindowsCredential` branch.

### Recommended Enterprise Process

#### 1. Review

Review the PowerShell script before running it in production or customer environments.

#### 2. Verify File Integrity

Each GitHub release publishes the SHA-256 of the shipped files in its release notes. Compute the hash of your download and compare it to the published value:

```powershell
Get-FileHash .\Get-SqlSafe.ps1 -Algorithm SHA256
Get-FileHash .\Get-SqlSafe.Azure.psm1 -Algorithm SHA256
```

The hashes must match the values in the release you downloaded. This is separate from the script's built-in SHA-256 check, which only verifies the embedded T-SQL against a value stored inside the script.

#### 3. Unblock Downloaded Files

```powershell
Unblock-File .\Get-SqlSafe.ps1
```

#### 4. Test First

Run the assessment against a non-production SQL Server instance before using it in a production environment.

#### 5. Re-sign Internally if Required

If your organization enforces `AllSigned`, sign the approved PowerShell file with your internal code-signing certificate after review.

Example only:

```powershell
$cert = Get-ChildItem Cert:\CurrentUser\My -CodeSigningCert | Select-Object -First 1
Set-AuthenticodeSignature -FilePath .\Get-SqlSafe.ps1 -Certificate $cert
```

Follow your internal process for code review, signing, packaging, and deployment.

---

## Scope and Limitations

The Community Edition is intentionally limited. It is not:

- A penetration test.
- A compliance assessment.
- A full SQL Server security review.
- A guarantee that the target SQL Server is secure.

A clean report means that the covered baseline indicators did not identify findings. SQL Server's real attack surface is broader and depends on combinations of permissions, ownership, impersonation, SQL Agent, linked servers, database configuration, service accounts, backups, operating-system security posture, and platform-specific controls.

Some checks may require permissions that are not available on older SQL Server versions or managed platforms without elevated access. Use the report as a starting point for deeper review and remediation planning.

---

## Upgrade from 2026.6

1. Replace `Get-SqlSafe.ps1` and, for Azure SQL Database, `Get-SqlSafe.Azure.psm1` together. Use a fresh PowerShell process afterwards.
2. Review the assessment login. The securityadmin-based setup of 2026.6 is no longer used: use **sysadmin** for a full assessment, or the limited grants under [Required SQL Server Permissions](#required-sql-server-permissions) and skip `046`, `050`, `069` and `072`. Remove securityadmin membership from a limited assessment login.
3. Expect different counts than in 2026.6 reports: Not assessed and Not checked entries are no longer counted, `129` and `130` now include online system databases, and `072`/`078` cover user databases only.
4. Wrappers that check exit codes: `4` and `5` are new.
5. Validate the new release on a non-production target before broader use.

## Upgrade Notes from 2026.5

1. Replace the old script with the 2026.7 `Get-SqlSafe.ps1` and use the updated README, changelog and license. SQL Server and RDS still require only the standalone script at runtime.
2. For Azure SQL Database, put `Get-SqlSafe.Azure.psm1` beside the script and install the Microsoft prerequisites described above.
3. Use a fresh PowerShell process after replacing the script, optional component or Microsoft modules. Already loaded .NET assemblies cannot be replaced inside the existing process.
4. Review the new Check `030`, the database categorization of `031`, and the changed treatment of skipped checks. A Not checked entry is not a PASS.
5. Validate the new release on a non-production target before broader use.

## Upgrade Notes from 2026.4

- Replace the previous collector with the new `Get-SqlSafe.ps1` file.
- Grant `CONNECT ANY DATABASE` to the assessment login if it does not have it. Check `130` needs it to enumerate `db_owner` membership across databases.
- Reports generated by 2026.4 remain readable. The report layout changes apply to newly generated reports only.
- Enable `-CreateIndividualDBLevelReports` only when per-database reports are wanted; the option adds one HTML file per database.

---

## Upgrade Notes from 2026.3

- Review [`CHANGELOG.md`](CHANGELOG.md) before replacing older scripts.
- Replace the previous collector with the new `Get-SqlSafe.ps1` file.
- Remove the old `SqlSafe.sql` file if it remains in a working folder; it is no longer used.
- Test the collector against a non-production SQL Server before broad use.
- Use `-AwsRdsCompat` when assessing SQL Server on Amazon RDS.

---

## Beyond the Baseline: Need the Complete Picture?

`Get-SqlSafe.ps1` covers a focused set of essential baseline indicators. Enterprise environments often require deeper architectural scrutiny.

The full **Sarpedon SQL Server Security Assessment** can include advanced architectural checks such as:

- Deep database-level configuration audits
- OS-level and backup security reviews
- Advanced account attribution and lateral-movement mapping
- High availability, operational, and governance-focused review areas

[Explore full-scope SQL Server security assessments at Sarpedon Quality Lab](https://sarpedonqualitylab.us/sql-server-security-assessment/).

Prefer to work through it yourself first? Use the free [SQL Server Security and High Availability Checklist](https://sarpedonqualitylab.us/resources/database-application-vendor-sql-server-security-high-availability-checklist/). For ongoing visibility into who changes what, see [SQL Server Auditing & Activity Monitoring](https://sarpedonqualitylab.us/services/#audit).

---

## License and Attribution

Logic & Engine by Andreas Wolter, former Microsoft Senior Program Manager for SQL Server security (MCSM: Data Platform), Sarpedon Quality Lab.

This project is distributed under the Sarpedon Community License. Use is permitted for internal business or personal purposes. Unmodified generated reports may be shared provided that all branding, attribution, Community Edition designation, and version information remain intact. Redistribution of modified scripts or reports is governed by the license terms.

See [`LICENSE.md`](LICENSE.md) for the full license text. Use the tool only on systems where you have authorization to run security assessment tooling.

---

## Disclaimer

This tool is provided "as is", without warranty of any kind.

It identifies indicators of risk and does not replace a full security audit, penetration test, compliance assessment, or professional security review.

Use at your own risk.
