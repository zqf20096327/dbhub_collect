# <img src="https://erikdarling.com/wp-content/uploads/2025/08/darling-data-logo_RGB.jpg" alt="Darling Data Logo" width="300"/>

# Darling Data: SQL Server Troubleshooting Scripts
<a name="header1"></a>
<p align="center">
  <a href="https://github.com/erikdarlingdata/DarlingData/stargazers"><img src="https://img.shields.io/github/stars/erikdarlingdata/DarlingData?style=for-the-badge&logo=github&color=gold&logoColor=black" alt="GitHub Stars"></a>
  <a href="https://github.com/erikdarlingdata/DarlingData/network/members"><img src="https://img.shields.io/github/forks/erikdarlingdata/DarlingData?style=for-the-badge&logo=github" alt="GitHub Forks"></a>
  <a href="https://github.com/erikdarlingdata/DarlingData/blob/main/LICENSE.md"><img src="https://img.shields.io/github/license/erikdarlingdata/DarlingData?style=for-the-badge" alt="License: MIT"></a>
  <a href="https://github.com/erikdarlingdata/DarlingData/releases/latest"><img src="https://img.shields.io/github/v/release/erikdarlingdata/DarlingData?style=for-the-badge" alt="Latest Release"></a>
  <a href="https://github.com/erikdarlingdata/DarlingData/issues"><img src="https://img.shields.io/github/issues/erikdarlingdata/DarlingData?style=for-the-badge" alt="Open Issues"></a>
  <a href="https://github.com/erikdarlingdata/DarlingData/commits/main"><img src="https://img.shields.io/github/last-commit/erikdarlingdata/DarlingData?style=for-the-badge" alt="Last Commit"></a>
  <a href="https://github.com/erikdarlingdata/DarlingData/actions/workflows/sql-tests.yml"><img src="https://img.shields.io/github/actions/workflow/status/erikdarlingdata/DarlingData/sql-tests.yml?style=for-the-badge&label=SQL%20Tests" alt="SQL Tests CI"></a>
</p>
<p align="center">
  <a href="https://x.com/erikdarlingdata"><img src="https://img.shields.io/badge/Follow_%40ErikDarlingData-black?style=for-the-badge&logo=x&logoColor=white" alt="Follow @ErikDarlingData on X"></a>
  <a href="https://www.youtube.com/@ErikDarlingData"><img src="https://img.shields.io/badge/YouTube-Subscribe-red?style=for-the-badge&logo=youtube&logoColor=white" alt="YouTube Subscribe"></a>
  <a href="https://www.linkedin.com/in/erik-darling-data/"><img src="https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn Connect"></a>
  <a href="https://erikdarling.com"><img src="https://img.shields.io/badge/Blog-erikdarling.com-FF6B35?style=for-the-badge&logo=wordpress&logoColor=white" alt="Blog"></a>
</p>

# Navigatory 
 - Scripts:
    - [sp_PressureDetector](#pressure-detector): Quickly detect CPU and memory pressure
    - [sp_PerfCheck](#perf-check): Comprehensive SQL Server performance health check
    - [sp_HumanEvents](#human-events): Use Extended Events to track down various query performance issues
    - [sp_HumanEventsBlockViewer](#human-events-block-viewer): Analyze the blocked process report
    - [sp_QuickieStore](#quickie-store): The fastest and most configurable way to navigate Query Store data
    - [sp_QuickieCache](#quickie-cache): High-impact query detection from the plan cache using Pareto analysis
    - [sp_QueryReproBuilder](#query-repro-builder): Generate executable reproduction scripts from Query Store data
    - [sp_HealthParser](#health-parser): Pull all the performance-related data from the system health Extended Event
    - [sp_LogHunter](#log-hunter): Get all of the worst stuff out of your error log
    - [sp_IndexCleanup](#index-cleanup): Identify unused and duplicate indexes
    - [sp_QueryStoreCleanup](#query-store-cleanup): Remove duplicate and noisy queries from Query Store

## Installing
To install every procedure in the list above except sp_QueryStoreCleanup, run [Install-All/DarlingData.sql](Install-All/DarlingData.sql). To install one procedure, run the .sql file in its folder. sp_QueryStoreCleanup is not in the bundle because it removes queries from Query Store. Install it from its own folder.

## Utility scripts
These folders each have their own READ

[...截断...]

ME:
 - [Clear Token Perm](Clear%20Token%20Perm): Monitor and clear the security token cache
 - [Export-SqlResults](Export-SqlResults): Run a query and export every result set to CSV
 - [Helper Views](Helper%20Views): Views and functions for diagnosing performance issues
 - [Ola Stats Only Job](Ola%20Stats%20Only%20Job): Agent job for nightly statistics updates with Ola Hallengren's solution
 - [ProtectSession](ProtectSession): Keep a session alive when it is blocked on lock waits
 - [sp_WhoIsActive Logging](sp_WhoIsActive%20Logging): Log sp_WhoIsActive output to tables
 - [String Functions](String%20Functions): Functions that extract or remove characters from strings
 - [TestBackupPerformance](TestBackupPerformance): Test backup settings to find the fastest combination

## Who are these scripts for?
You need to troubleshoot performance problems with SQL Server, and you need to do it now. 

You don't have time to track down a bunch of DMVs, figure out Extended Events, wrestle with terrible SSMS interfaces, or learn XML.

These scripts aren't a replacement for a mature monitoring tool, but they do a good job of capturing important issues and reporting on existing diagnostic data

## Support
Right now, all support and Q&A is handled on GitHub. Please be patient; it's just me over here answering questions, fixing bugs, and adding new features.

As far as compatibility goes, they're only guaranted to work on Microsoft-supported SQL Server versions.

Older versions are either missing too much information, or simply aren't compatible (Hello, Extended Events. Hello, Query Store) with the intent of the script.

If you have questions about performance tuning, or SQL Server in general, you'll wanna hit a Q&A site:
 * [Top Answers](https://topanswers.xyz/databases)
 * [DBA Stack Exchange](https://dba.stackexchange.com/)

[*Back to top*](#navigatory)

## Pressure Detector

Is your client/server relationship on the rocks? Are queries timing out, dragging along, or causing CPU fans to spin out of control?

All you need to do is hit F5 to get information about:
 * Wait stats since startup
 * Database file size, stall, and activity
 * tempdb configuration details
 * Memory consumers
 * Low memory indicators
 * Memory configuration and allocation
 * Current query memory grants, along with other execution details
 * CPU configuration and retained utilization details
 * Thread count and current usage 
 * Any current THREADPOOL waits (best observed with the DAC)
 * Currently executing queries, along with other execution details
 * Blocking chains with lead blockers (@troubleshoot_blocking = 1)
 * Optional logging to permanent tables (@log_to_table = 1)

For a video walkthrough of the script and the results, [head over here](https://www.erikdarling.com/sp_pressuredetector/).

Current valid parameter details:

|       parameter_name       | data_type |                                  description                                   |                     valid_inputs                     |   defaults   |
|----------------------------|-----------|--------------------------------------------------------------------------------|------------------------------------------------------|--------------|
| @what_to_check             | varchar   | areas to check for pressure                                                    | "all", "cpu", and "memory"                           | all          |
| @skip_queries              | bit       | if you want to skip looking at running queries                                 | 0 or 1                                               | 0            |
| @skip_plan_xml             | bit       | if you want to skip getting plan XML                                           | 0 or 1                                               | 0            |
| @minimum_disk_latency_ms   | smallint  | low bound for reporting disk latency                                           | a reasonable number of milliseconds for disk latency | 100         